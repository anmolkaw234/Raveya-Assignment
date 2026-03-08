from typing import List
from pydantic import BaseModel, Field


class ProposalRequest(BaseModel):
    buyer_name: str = Field(..., min_length=2)
    buyer_type: str = Field(..., min_length=2)
    budget: int = Field(..., gt=0)
    goals: List[str] = Field(..., min_length=1)
    preferred_categories: List[str] = Field(default_factory=list)
    sustainability_focus: List[str] = Field(default_factory=list)


class ProductMixItem(BaseModel):
    product_name: str
    category: str
    quantity: int = Field(..., gt=0)
    unit_price: int = Field(..., gt=0)
    line_total: int = Field(..., gt=0)
    sustainability_note: str


class CostBreakdown(BaseModel):
    subtotal: int
    packaging: int
    logistics: int
    total: int


class ProposalResult(BaseModel):
    recommended_product_mix: List[ProductMixItem] = Field(..., min_length=1)
    cost_breakdown: CostBreakdown
    impact_positioning_summary: str


class ProposalResponse(BaseModel):
    id: int
    buyer_name: str
    result: ProposalResult
