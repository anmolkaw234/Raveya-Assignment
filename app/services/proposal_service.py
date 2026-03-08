from sqlalchemy.orm import Session

from app.models.entities import Proposal
from app.schemas.proposal import ProposalRequest, ProposalResult
from app.services.ai_client import AIClient
from app.services.logger_service import LoggerService


class ProposalService:
    def __init__(self) -> None:
        self.ai_client = AIClient()

    def _fallback(self, payload: ProposalRequest) -> dict:
        preferred = payload.preferred_categories or ["stationery", "packaging"]

        items = []
        subtotal = 0

        if "stationery" in [c.lower() for c in preferred]:
            items.append(
                {
                    "product_name": "Recycled Paper Notebooks",
                    "category": "stationery",
                    "quantity": 100,
                    "unit_price": 120,
                    "line_total": 12000,
                    "sustainability_note": "Made from recycled paper and suitable for bulk gifting.",
                }
            )
            subtotal += 12000

            items.append(
                {
                    "product_name": "Bamboo Pens",
                    "category": "stationery",
                    "quantity": 200,
                    "unit_price": 40,
                    "line_total": 8000,
                    "sustainability_note": "Lower plastic usage and strong eco-brand appeal.",
                }
            )
            subtotal += 8000

        if "packaging" in [c.lower() for c in preferred]:
            items.append(
                {
                    "product_name": "Kraft Gift Boxes",
                    "category": "packaging",
                    "quantity": 100,
                    "unit_price": 90,
                    "line_total": 9000,
                    "sustainability_note": "Plastic-light packaging with recyclable material.",
                }
            )
            subtotal += 9000

        if not items:
            items.append(
                {
                    "product_name": "Eco Starter Gift Set",
                    "category": "corporate gifting",
                    "quantity": 100,
                    "unit_price": 200,
                    "line_total": 20000,
                    "sustainability_note": "Balanced starter option for sustainable procurement.",
                }
            )
            subtotal += 20000

        packaging = int(subtotal * 0.08)
        logistics = int(subtotal * 0.06)
        total = subtotal + packaging + logistics

        if total > payload.budget:
            # Simple budget trimming: reduce quantities proportionally
            ratio = payload.budget / total
            trimmed_items = []
            new_subtotal = 0

            for item in items:
                new_qty = max(1, int(item["quantity"] * ratio))
                new_line_total = new_qty * item["unit_price"]
                trimmed = {
                    **item,
                    "quantity": new_qty,
                    "line_total": new_line_total,
                }
                trimmed_items.append(trimmed)
                new_subtotal += new_line_total

            items = trimmed_items
            subtotal = new_subtotal
            packaging = int(subtotal * 0.08)
            logistics = int(subtotal * 0.06)
            total = subtotal + packaging + logistics

        return {
            "recommended_product_mix": items,
            "cost_breakdown": {
                "subtotal": subtotal,
                "packaging": packaging,
                "logistics": logistics,
                "total": total,
            },
            "impact_positioning_summary": (
                f"A sustainable proposal for a {payload.buyer_type} buyer focused on "
                f"{', '.join(payload.goals)} while staying within budget."
            ),
        }

    def generate_proposal(self, db: Session, payload: ProposalRequest) -> Proposal:
        system_prompt = (
            "You are a B2B sustainable commerce proposal assistant. "
            "Return strict JSON with keys: recommended_product_mix, cost_breakdown, impact_positioning_summary. "
            "Each product mix item must contain product_name, category, quantity, unit_price, line_total, sustainability_note. "
            "cost_breakdown must contain subtotal, packaging, logistics, total. "
            "Ensure total does not exceed the provided budget."
        )

        user_prompt = (
            f"Buyer name: {payload.buyer_name}\n"
            f"Buyer type: {payload.buyer_type}\n"
            f"Budget: {payload.budget}\n"
            f"Goals: {', '.join(payload.goals)}\n"
            f"Preferred categories: {', '.join(payload.preferred_categories)}\n"
            f"Sustainability focus: {', '.join(payload.sustainability_focus)}"
        )

        try:
            raw = self.ai_client.generate_json(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
            )
        except Exception:
            raw = self._fallback(payload)

        validated = ProposalResult.model_validate(raw)

        saved = Proposal(
            buyer_name=payload.buyer_name,
            buyer_type=payload.buyer_type,
            budget=payload.budget,
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
            request_payload=payload.model_dump(),
            prompt_text=user_prompt,
            response_payload=validated.model_dump(),
        )

        return saved