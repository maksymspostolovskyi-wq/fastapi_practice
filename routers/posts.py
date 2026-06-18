import logging

from fastapi import APIRouter, Depends, HTTPException, status

from schemas.post import PostCreate, PostRead, PostUpdate
from services.posts import PostService, get_post_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=list[PostRead])
async def get_posts(
    post_service: PostService = Depends(get_post_service),
):
    try:
        return await post_service.get_all()
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Failed to get posts")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get posts",
        ) from exc


@router.get("/{post_id}", response_model=PostRead)
async def get_post(
    post_id: int,
    post_service: PostService = Depends(get_post_service),
):
    try:
        post = await post_service.get_by_id(post_id=post_id)
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found",
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


@router.post("/", response_model=PostRead, status_code=status.HTTP_201_CREATED)
async def create_post(
    post_data: PostCreate,
    post_service: PostService = Depends(get_post_service),
):
    try:
        return await post_service.create(data=post_data)
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Failed to create post")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create post",
        ) from exc


@router.put("/{post_id}", response_model=PostRead)
async def update_post(
    post_id: int,
    post_update: PostUpdate,
    post_service: PostService = Depends(get_post_service),
):
    try:
        post = await post_service.update(post_id=post_id, data=post_update)
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found",
            )
        return post
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Failed to update post with id %d", post_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update post",
        ) from exc


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: int,
    post_service: PostService = Depends(get_post_service),
):
    try:
        deleted = await post_service.delete(post_id=post_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found",
            )
        return None
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Failed to delete post with id %d", post_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete post",
        ) from exc
