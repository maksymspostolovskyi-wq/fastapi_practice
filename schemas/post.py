from typing import Optional

from pydantic import BaseModel, Field


class PostCreate(BaseModel):
    title: str = Field(max_length=255)
    content: str
    author_id: int = Field(gt=0)


class PostRead(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    author_id: int

    class Config:
        from_attributes = (
            True  # Дозволяє зчитувати дані з моделей SQLAlchemy [cite: 58]
        )


class PostUpdate(BaseModel):
    title: Optional[str] = Field(default=None, max_length=255)
    content: Optional[str] = Field(default=None)
    published: Optional[bool] = Field(default=None)
