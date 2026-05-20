import re
import secrets
from hashlib import sha256
from typing import Annotated

from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel, EmailStr
from tortoise.context import TortoiseContext

from app.orm.helpers import build_schema_config, migrate_tenant
from app.orm.models.super import Tenant
from app.orm.models.tenant import User

router = APIRouter(prefix="/platform", tags=["platform"])


class RegisterRequest(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    tenant_name: str


class RegisterResponse(BaseModel):
    tenant_id: str
    user_id: int


def _to_schema_name(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")
    if not slug:
        slug = "tenant"

    return f"tenant_{slug}"


@router.post("/register", response_model=RegisterResponse)
async def register_user(
    payload: RegisterRequest,
    tenant_id: Annotated[str, Header()],
) -> RegisterResponse:
    if tenant_id.lower() != "super":
        raise HTTPException(
            status_code=400,
            detail="Registration actions must run through management administration contexts",
        )

    schema = _to_schema_name(payload.tenant_name)
    if await Tenant.exists(schema=schema):
        schema = f"{schema}_{secrets.token_hex(2)}"

    tenant = await Tenant.create(name=payload.tenant_name, schema=schema)
    await migrate_tenant(schema=schema)

    password_hash = sha256(payload.password.encode()).hexdigest()

    tenant_config = build_schema_config(schema)
    async with TortoiseContext() as ctx:
        await ctx.init(config=tenant_config)
        try:
            user = await User.create(
                name=payload.full_name,
                email=payload.email.lower(),
                password=password_hash,
            )
        finally:
            await ctx.close_connections()

    return RegisterResponse(tenant_id=tenant.schema, user_id=user.id)
