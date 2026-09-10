from sqlalchemy import Column, String, Text, DateTime
from blog.db import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone

class Post(Base):
    __tablename__ = "posts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False, unique=True)
    slug = Column(String(255), nullable=False, unique=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    image_url = Column(Text, nullable=True)