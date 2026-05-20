from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Header
from tortoise.context import TortoiseContext

from app import __version__, __display_name__, routers
from app.orm.helpers import build_schema_config
from app.orm.models.super import Tenant


async def set_db_context(tenant_id: Annotated[str, Header()]):
    schema = tenant_id.lower()

    if schema != "super":
        super_config = build_schema_config("super")
        async with TortoiseContext() as ctx:
            await ctx.init(config=super_config)
            try:
                if not await Tenant.exists(schema=schema):
                    raise HTTPException(status_code=404, detail="Tenant not found")
            finally:
                await ctx.close_connections()

    config = build_schema_config(schema)
    async with TortoiseContext() as ctx:
        await ctx.init(config=config)
        try:
            yield
        finally:
            await ctx.close_connections()


application = FastAPI(title=__display_name__, version=__version__)

application.include_router(routers.routes, dependencies=[Depends(set_db_context)])
