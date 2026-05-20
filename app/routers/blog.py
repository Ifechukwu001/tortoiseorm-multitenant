from hashlib import sha256

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr

from app.orm.models.tenant import Blog, User

router = APIRouter(prefix="/blogs", tags=["blogs"])


class BlogCreateRequest(BaseModel):
    email: EmailStr
    auth_key: str
    title: str
    content: str


class BlogResponse(BaseModel):
    id: int
    title: str
    content: str
    author_email: str


async def _authenticate(email: str, auth_key: str) -> User:
    user = await User.get_or_none(email=email.lower())
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    expected = sha256(f"{email.lower()}:{user.password}".encode()).hexdigest()
    if expected != auth_key:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return user


@router.post("", response_model=BlogResponse)
async def create_blog(payload: BlogCreateRequest) -> BlogResponse:
    user = await _authenticate(email=payload.email, auth_key=payload.auth_key)

    blog = await Blog.create(user=user, title=payload.title, content=payload.content)
    return BlogResponse(
        id=blog.id,
        title=blog.title,
        content=blog.content,
        author_email=user.email,
    )


@router.post("/list", response_model=list[BlogResponse])
async def list_blogs() -> list[BlogResponse]:
    blogs = await Blog.all().prefetch_related("user").order_by("-created_at")
    return [
        BlogResponse(
            id=blog.id,
            title=blog.title,
            content=blog.content,
            author_email=blog.user.email,
        )
        for blog in blogs
    ]
