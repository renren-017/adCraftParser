from pydantic import BaseModel, Field
from typing import List


class CategoryFields(BaseModel):
    search_keys: List[str] = Field(default=[], description="List of search keys")
