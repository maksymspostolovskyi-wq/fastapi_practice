import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.post import Post
from schemas.post import PostCreate, PostRead, PostUpdate
from settings.db import get_db

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/posts", tags=["Posts"])

SessionDepend = Annotated[AsyncSession, Depends(get_db)]


# 1. Отримання всіх статей (READ) [cite: 77]
@router.get("/", response_model=list[PostRead])
async def get_posts(session: SessionDepend):
    try:
        result = await session.execute(select(Post))
        return result.scalars().all()
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Failed to get posts")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get posts",
        ) from exc


# 2. Отримання однієї статті за ID (READ) [cite: 78]
@router.get("/{post_id}", response_model=PostRead)
async def get_post(post_id: int, session: SessionDepend):
    try:
        result = await session.execute(select(Post).where(Post.id == post_id))
        post = result.scalars().first()

        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
            )
        return post
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Failed to get post with id %d", post_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get post",
        ) from exc


# 3. Створення статті (CREATE) [cite: 79]
@router.post("/", response_model=PostRead, status_code=status.HTTP_201_CREATED)
async def create_post(post_data: PostCreate, session: SessionDepend):
    try:
        new_post = Post(**post_data.model_dump())
        session.add(new_post)
        await session.commit()
        await session.refresh(new_post)
        return new_post
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Failed to create post")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create post",
        ) from exc


# 4. Оновлення статті (UPDATE) [cite: 80]
@router.put("/{post_id}", response_model=PostRead)
async def update_post(post_id: int, post_update: PostUpdate, session: SessionDepend):
    try:
        result = await session.execute(select(Post).where(Post.id == post_id))
        existing_post = result.scalars().first()

        if not existing_post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
            )

        for field, value in post_update.model_dump(exclude_unset=True).items():
            setattr(existing_post, field, value)

        session.add(existing_post)
        await session.commit()
        await session.refresh(existing_post)
        return existing_post
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Failed to update post with id %d", post_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update post",
        ) from exc


# 5. Видалення статті (DELETE) [cite: 81]
@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int, session: SessionDepend):
    try:
        result = await session.execute(select(Post).where(Post.id == post_id))
        existing_post = result.scalars().first()

        if not existing_post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
            )

        await session.delete(existing_post)
        await session.commit()
        return None
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Failed to delete post with id %d", post_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete post",
        ) from exc
