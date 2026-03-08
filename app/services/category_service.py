from sqlalchemy.orm import Session

from app.models.entities import ProductAnalysis
from app.schemas.category import CategoryResult, ProductInput
from app.services.ai_client import AIClient
from app.services.logger_service import LoggerService


class CategoryService:
    def __init__(self) -> None:
        self.ai_client = AIClient()

    def _fallback(self, product: ProductInput) -> dict:
        text = f"{product.name} {product.description} {product.material or ''}".lower()
        if any(word in text for word in ["bottle", "mug", "cup"]):
            primary = "Drinkware"
            sub = "Reusable Bottles"
            filters = ["Reusable", "Low Waste"]
        elif any(word in text for word in ["notebook", "paper", "journal", "pencil"]):
            primary = "Stationery"
            sub = "Eco Stationery"
            filters = ["Recycled", "Plastic Free"]
        elif any(word in text for word in ["bag", "tote"]):
            primary = "Bags"
            sub = "Reusable Totes"
            filters = ["Reusable", "Natural Fiber"]
        else:
            primary = "Corporate Gifting"
            sub = "Sustainable Essentials"
            filters = ["Eco Friendly", "Reusable"]

        tags = [
            product.name.lower().replace(" ", "-"),
            "sustainable",
            "eco-friendly",
            primary.lower().replace(" ", "-"),
            sub.lower().replace(" ", "-"),
        ]
        return {
            "primary_category": primary,
            "sub_category": sub,
            "seo_tags": tags[:5],
            "sustainability_filters": filters,
        }

    def analyze_product(self, db: Session, product: ProductInput) -> ProductAnalysis:
        system_prompt = (
            "You are an ecommerce merchandising assistant for sustainable commerce. "
            "Return strict JSON with keys: primary_category, sub_category, seo_tags, sustainability_filters. "
            "seo_tags must be 5 to 10 short lowercase tags. sustainability_filters must be 2 to 6 buyer-facing filters."
        )
        user_prompt = (
            f"Product data:\n"
            f"name: {product.name}\n"
            f"description: {product.description}\n"
            f"material: {product.material}\n"
            f"target_customer: {product.target_customer}\n"
            f"price_in_inr: {product.price_in_inr}"
        )

        try:
            raw = self.ai_client.generate_json(system_prompt=system_prompt, user_prompt=user_prompt)
        except Exception:
            raw = self._fallback(product)

        validated = CategoryResult.model_validate(raw)
        saved = ProductAnalysis(
            product_name=product.name,
            primary_category=validated.primary_category,
            sub_category=validated.sub_category,
            seo_tags=validated.seo_tags,
            sustainability_filters=validated.sustainability_filters,
        )
        db.add(saved)
        db.commit()
        db.refresh(saved)

        LoggerService.log_prompt_response(
            db,
            module="auto-category-tag-generator",
            request_payload=product.model_dump(),
            prompt_text=user_prompt,
            response_payload=validated.model_dump(),
        )
        return saved
