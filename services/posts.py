from typing import Sequence

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.post import Post
from schemas.post import PostCreate, PostUpdate
from settings.db import get_db


class PostService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> Sequence[Post]:
        result = await self.db.execute(select(Post))
        return result.scalars().all()

    async def get_by_id(self, post_id: int) -> Post | None:
        result = await self.db.execute(select(Post).where(Post.id == post_id))
        return result.scalars().first()

    async def create(self, data: PostCreate) -> Post:
        new_post = Post(**data.model_dump())
        self.db.add(new_post)
        await self.db.commit()
        await self.db.refresh(new_post)
        return new_post

    async def update(self, post_id: int, data: PostUpdate) -> Post | None:
        post = await self.get_by_id(post_id)
        if not post:
            return None

        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(post, field, value)

        self.db.add(post)
        await self.db.commit()
        await self.db.refresh(post)
        return post

    async def delete(self, post_id: int) -> bool:
        post = await self.get_by_id(post_id)
        if not post:
            return False

        await self.db.delete(post)
        await self.db.commit()
        return True


async def get_post_service(
    db: AsyncSession = Depends(get_db),
) -> PostService:
    return PostService(db)
