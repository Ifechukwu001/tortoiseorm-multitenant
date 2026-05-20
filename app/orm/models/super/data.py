from tortoise import fields, models


class Tenant(models.Model):
    id = fields.BigIntField(primary_key=True)
    name = fields.CharField(max_length=255)
    schema = fields.CharField(max_length=255, unique=True)


class PlatformAdmin(models.Model):
    id = fields.BigIntField(primary_key=True)
    name = fields.CharField(max_length=255)
    email = fields.CharField(max_length=255, unique=True)
    password = fields.CharField(max_length=255)
