import sys

from tortoise import run_async

from app.orm.helpers import migrate_super


def main(migration: str | None = None) -> None:
    """Script entrypoint for migrating the super schema.

    Args:
        migration: Optional specific migration to apply.
    """

    run_async(migrate_super(target=migration))


if __name__ == "__main__":
    migration = sys.argv[1] if len(sys.argv) > 1 else None

    main(migration)
