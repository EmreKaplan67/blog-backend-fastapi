from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from uuid import UUID

class PostCreate(BaseModel):
    title: str = Field(..., max_length=255)
    content: str
    image_url: str | None = None

class PostUpdate(BaseModel):
    title: str | None = Field(None, max_length=255)
    content: str | None = None
    image_url: str | None = None

class PostResponse(BaseModel):
    id: UUID
    title: str
    slug: str
    content: str
    image_url: str | None = None
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)