import sys

from tortoise import run_async

from app.orm.helpers import get_tenant_schemas, migrate_tenant


def main(migration: str | None = None) -> None:
    """Script entrypoint for migrating tenant schemas.

    Args:
        migration: Optional specific migration to apply.
    """

    async def _() -> None:
        schemas = await get_tenant_schemas()

        for schema in schemas:
            await migrate_tenant(schema=schema, target=migration)

    run_async(_())


if __name__ == "__main__":
    migration = sys.argv[1] if len(sys.argv) > 1 else None

    main(migration)
