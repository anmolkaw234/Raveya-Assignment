from sqlalchemy.orm import Session

from app.models.entities import Proposal
from app.schemas.proposal import ProposalRequest, ProposalResult
from app.services.ai_client import AIClient
from app.services.logger_service import LoggerService
from app.utils.catalog import CATALOG


class ProposalService:
    def __init__(self) -> None:
        self.ai_client = AIClient()

    def _fallback(self, request: ProposalRequest) -> dict:
        items = []
        running_total = 0
        for item in CATALOG:
            qty = max(1, request.budget // (len(CATALOG) * item["unit_price"]))
            line_total = qty * item["unit_price"]
            running_total += line_total
            items.append(
                {
                    "product_name": item["product_name"],
                    "category": item["category"],
                    "quantity": qty,
                    "unit_price": item["unit_price"],
                    "line_total": line_total,
                    "sustainability_note": item["sustainability_note"],
                }
            )

        packaging = max(1000, int(request.budget * 0.03))
        logistics = max(1500, int(request.budget * 0.05))
        total = running_total + packaging + logistics
        if total > request.budget:
            diff = total - request.budget
            items[-1]["quantity"] = max(1, items[-1]["quantity"] - max(1, diff // items[-1]["unit_price"]))
            items[-1]["line_total"] = items[-1]["quantity"] * items[-1]["unit_price"]
            running_total = sum(x["line_total"] for x in items)
            total = running_total + packaging + logistics

        return {
            "recommended_product_mix": items,
            "cost_breakdown": {
                "subtotal": running_total,
                "packaging": packaging,
                "logistics": logistics,
                "total": total,
            },
            "impact_positioning_summary": (
                f"This proposal for {request.buyer_name} balances useful branded merchandise with reusable, "
                f"lower-waste products that support visible sustainability messaging for {request.buyer_type} buyers."
            ),
        }

    def generate_proposal(self, db: Session, request: ProposalRequest) -> Proposal:
        system_prompt = (
            "You are a B2B sustainable commerce proposal assistant. "
            "Return strict JSON with keys: recommended_product_mix, cost_breakdown, impact_positioning_summary. "
            "Each product mix item must contain product_name, category, quantity, unit_price, line_total, sustainability_note."
        )
        user_prompt = (
            f"Buyer name: {request.buyer_name}\n"
            f"Buyer type: {request.buyer_type}\n"
            f"Budget: {request.budget}\n"
            f"Goals: {', '.join(request.goals)}\n"
            f"Preferred categories: {', '.join(request.preferred_categories)}\n"
            f"Sustainability focus: {', '.join(request.sustainability_focus)}\n"
            f"Available catalog: {CATALOG}"
        )

        try:
            raw = self.ai_client.generate_json(system_prompt=system_prompt, user_prompt=user_prompt)
        except Exception:
            raw = self._fallback(request)

        validated = ProposalResult.model_validate(raw)
        saved = Proposal(
            buyer_name=request.buyer_name,
            budget=request.budget,
            product_mix=[item.model_dump() for item in validated.recommended_product_mix],
            cost_breakdown=validated.cost_breakdown.model_dump(),
            impact_positioning_summary=validated.impact_positioning_summary,
        )
        db.add(saved)
        db.commit()
        db.refresh(saved)

        LoggerService.log_prompt_response(
            db,
            module="b2b-proposal-generator",
            request_payload=request.model_dump(),
            prompt_text=user_prompt,
            response_payload=validated.model_dump(),
        )
        return saved
