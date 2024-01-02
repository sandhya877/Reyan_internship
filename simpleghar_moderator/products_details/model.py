
from pydantic import BaseModel
from typing import List, Dict, Optional

class Category(BaseModel):
    id: str
    path: List[str]
    products: List[str]
    childs: List[Dict]
    name: str
    depth: int

class Moderator(BaseModel):
    name: str
    article_ids: List[str] = []

class ProductURLDetails(BaseModel):
    url: str
    tag: Optional[str] = ""  # Assuming a tag field for each URL

class Article(BaseModel):
    title: str
    parent_tag: List[str]
    child_tag: List[str]
    product_urls: List[ProductURLDetails]
    moderator_name: str

