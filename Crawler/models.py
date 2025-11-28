from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Book(BaseModel):
    title: str
    description: Optional[str]
    category: Optional[str]
    price_incl_tax: Optional[float]
    price_excl_tax: Optional[float]
    availability: Optional[str]
    num_reviews: Optional[int]
    image_url: Optional[str]
    rating: Optional[int]
    
    #metadata
    source_url: str
    html_snapshot: Optional[str] = None
    crawl_timestamp: datetime = Field(default_factory=datetime.utcnow)
    status: str = "success"
    content_hash: Optional[str] = None  # used for change detection