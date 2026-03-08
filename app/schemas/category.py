from typing import List

from pydantic import BaseModel


class ProductInput(BaseModel):
    product_name: str
    description: str
    materials: List[str]
    price: float
    target_market: str


class CategoryResult(BaseModel):
    primary_category: str
    sub_category: str
    seo_tags: List[str]
    sustainability_filters: List[str]


class CategoryResponse(BaseModel):
    id: int
    product_name: str
    result: CategoryResult