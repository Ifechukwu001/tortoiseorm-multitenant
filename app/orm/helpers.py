# pyright: reportReturnType=none
import copy
from typing import Any

from tortoise.context import TortoiseContext
from tortoise.connection import get_connection
from tortoise.migrations.api import migrate
from tortoise.migrations.recorder import MigrationRecorder

from .config import TORTOISE_CONFIG


def build_schema_config(schema: str) -> dict[str, Any]:
    """Build a config for the schema from the base config."""
    config = copy.deepcopy(TORTOISE_CONFIG)
    config["connections"]["default"]["credentials"]["schema"] = schema
    if schema == "super":
        del config["apps"]["tenant"]
    else:
        del config["apps"]["super"]

    return config


async def get_tenant_schemas() -> list[str]:
    """Load tenant schemas from the super tenant table."""
    async with TortoiseContext() as ctx:
        super_config = build_schema_config("super")
        await ctx.init(config=super_config)

        from .models.super import Tenant

        schemas = await Tenant.all().values_list("schema", flat=True)
        await ctx.close_connections()
        return schemas


async def ensure_schema_exists(ctx: TortoiseContext, schema: str) -> None:
    """Ensure that the given schema exists in the database."""
    connection = get_connection("default")
    await connection.execute_query(f'CREATE SCHEMA IF NOT EXISTS "{schema}"')


async def migrate_tenant(
    schema: str,
    target: str | None = None,
) -> None:
    """Migrate a single tenant schema."""
    async with TortoiseContext() as ctx:
        tenant_config = build_schema_config(schema)
        await ctx.init(config=tenant_config)

        await ensure_schema_exists(ctx, schema)

        await migrate(
            config=tenant_config,
            app_labels=["tenant"],
            target=f"tenant.{target}" if target else None,
        )

        await ctx.close_connections()


async def migrate_super(target: str | None = None) -> None:
    """Migrate the super schema."""
    async with TortoiseContext() as ctx:
        super_config = build_schema_config("super")
        await ctx.init(config=super_config)

        await ensure_schema_exists(ctx, "super")

        await migrate(
            config=super_config,
            app_labels=["super"],
            target=f"super.{target}" if target else None,
        )

        await ctx.close_connections()


async def migration_history(schema: str) -> list[str]:
    """Get the list of applied migrations for the given tenant schema."""
    async with TortoiseContext() as ctx:
        tenant_config = build_schema_config(schema)
        await ctx.init(config=tenant_config)

        await ensure_schema_exists(ctx, schema)

        recorder = MigrationRecorder(get_connection("default"))
        applied = await recorder.applied_migrations()

        await ctx.close_connections()
        return [f"{migration.app_label}.{migration.name}" for migration in applied]
