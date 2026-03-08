from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.category import CategoryResponse, ProductInput
from app.schemas.common import HealthResponse
from app.schemas.proposal import ProposalRequest, ProposalResponse
from app.services.category_service import CategoryService
from app.services.proposal_service import ProposalService

router = APIRouter()


@router.get("/")
def root():
    return {"message": "Rayeva AI Assignment API is running"}


@router.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    return HealthResponse()


@router.post("/ai/category-tags", response_model=CategoryResponse)
def generate_category_tags(
    payload: ProductInput,
    db: Session = Depends(get_db),
) -> CategoryResponse:
    saved = CategoryService().analyze_product(db, payload)
    return CategoryResponse(
        id=saved.id,
        product_name=saved.product_name,
        result={
            "primary_category": saved.primary_category,
            "sub_category": saved.sub_category,
            "seo_tags": saved.seo_tags,
            "sustainability_filters": saved.sustainability_filters,
        },
    )


@router.post("/ai/proposals", response_model=ProposalResponse)
def generate_proposal(
    payload: ProposalRequest,
    db: Session = Depends(get_db),
) -> ProposalResponse:
    saved = ProposalService().generate_proposal(db, payload)
    return ProposalResponse(
        id=saved.id,
        buyer_name=saved.buyer_name,
        result={
            "recommended_product_mix": saved.product_mix,
            "cost_breakdown": saved.cost_breakdown,
            "impact_positioning_summary": saved.impact_positioning_summary,
        },
    )