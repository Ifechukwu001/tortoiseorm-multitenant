from app.env import environment

TORTOISE_CONFIG = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.asyncpg",
            "credentials": {
                "host": environment.DB_HOST,
                "port": environment.DB_PORT,
                "user": environment.DB_USER,
                "password": environment.DB_PASSWORD,
                "database": environment.DB_NAME,
            },
        }
    },
    "apps": {
        "super": {
            "models": ["app.orm.models.super"],
            "default_connection": "default",
            "migrations": "app.orm.migrations.super",
        },
        "tenant": {
            "models": ["app.orm.models.tenant"],
            "default_connection": "default",
            "migrations": "app.orm.migrations.tenant",
        },
    },
}
