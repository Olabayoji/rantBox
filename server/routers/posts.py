from fastapi import APIRouter
from global_context.context import db_dependency, user_dependency
from fastapi import status
from fastapi.exceptions import HTTPException

from models import Post
from validations.validations import CreatePostRequest, GetPostResponse


post_router = APIRouter()


# get all posts for a user
@post_router.get(
    "/",
    status_code=status.HTTP_200_OK,
    tags=["posts"],
    response_model=list[GetPostResponse],
)
async def get_posts(db: db_dependency, user: user_dependency):
    print(user)
    posts = db.query(Post).filter(Post.user_id == user["user_id"]).all()
    return posts


# create a new post
@post_router.post(
    "/", status_code=status.HTTP_201_CREATED, tags=["posts"], response_model=None
)
async def create_post(
    db: db_dependency, user: user_dependency, post: CreatePostRequest
):
    new_post = Post(title=post.title, content=post.content, user_id=user["user_id"])
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return


# update a post
@post_router.put(
    "/{post_id}", status_code=status.HTTP_200_OK, tags=["posts"], response_model=None
)
async def update_post(
    db: db_dependency, user: user_dependency, post_id: int, post: CreatePostRequest
):
    post_data = db.query(Post).filter(Post.id == post_id).first()
    if not post_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    if post_data.user_id != int(user["user_id"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User not authorized"
        )
    post_data.title = post.title
    post_data.content = post.content
    db.commit()
    return
