from datetime import datetime
from pydantic import BaseModel, Field

class ScrapedRecord(BaseModel):
    source: str = "demo-dynamic-site"
    external_id: str = Field(min_length=3)
    title: str = Field(min_length=3)
    category: str = Field(min_length=2)
    price: float = Field(ge=0)
    rating: float = Field(ge=0, le=5)
    url: str
    captured_at: datetime = Field(default_factory=datetime.utcnow)
