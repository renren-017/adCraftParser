from typing import List
from pydantic import BaseModel

from app.models.schemas.categories.base import CategoryFields


__all__ = [
    "CategoryParse"
]


class CategoryParse(BaseModel):
    search_keys: List[str]
