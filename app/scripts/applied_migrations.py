import sys

from tortoise import run_async

from app.orm.helpers import get_tenant_schemas, migration_history


def main(schema: str | None = None) -> None:
    """Script entrypoint for displaying migration history for schemas.

    Args:
        schema: Optional specific schema to display migration history for.
    """

    async def _(schema: str | None) -> None:
        schemas: list[str] = ["super"]

        if not schema:
            schemas.extend(await get_tenant_schemas())

        else:
            schemas = [schema]

        schema_histories: dict[str, list[str]] = {}
        for schema in schemas:
            schema_histories[schema] = await migration_history(schema=schema)

        for schema, history in schema_histories.items():
            print(f"Migration history for schema '{schema}':")
            for migration in history:
                print(f"  - {migration}")

    run_async(_(schema))


if __name__ == "__main__":
    schema = sys.argv[1] if len(sys.argv) > 1 else None

    main(schema)
