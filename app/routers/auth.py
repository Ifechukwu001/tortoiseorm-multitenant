from hashlib import sha256

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr

from app.orm.models.tenant import User

router = APIRouter(prefix="/auth", tags=["auth"])


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    user_id: int
    auth_key: str


@router.post("/login", response_model=LoginResponse)
async def login(payload: LoginRequest) -> LoginResponse:
    email = payload.email.lower()
    password_hash = sha256(payload.password.encode("utf-8")).hexdigest()

    user = await User.get_or_none(email=email)
    if not user or user.password != password_hash:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    auth_key = sha256(f"{email}:{user.password}".encode()).hexdigest()
    return LoginResponse(user_id=user.id, auth_key=auth_key)
