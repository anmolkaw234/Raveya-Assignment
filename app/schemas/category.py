from typing import List
from pydantic import BaseModel, Field


class ProductInput(BaseModel):
    name: str = Field(..., min_length=2)
    description: str = Field(..., min_length=10)
    material: str | None = None
    target_customer: str | None = None
    price_in_inr: int | None = Field(default=None, ge=0)


class CategoryResult(BaseModel):
    primary_category: str
    sub_category: str
    seo_tags: List[str] = Field(min_length=5, max_length=10)
    sustainability_filters: List[str] = Field(min_length=2, max_length=6)


class CategoryResponse(BaseModel):
    id: int
    product_name: str
    result: CategoryResult
