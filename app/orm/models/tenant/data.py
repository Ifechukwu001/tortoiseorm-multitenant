from tortoise import fields, models


class User(models.Model):
    id = fields.BigIntField(primary_key=True)
    name = fields.CharField(max_length=255)
    email = fields.CharField(max_length=255, unique=True)
    password = fields.CharField(max_length=255)


class Blog(models.Model):
    id = fields.BigIntField(primary_key=True)
    user = fields.ForeignKeyField("tenant.User", related_name="blogs")
    title = fields.CharField(max_length=255)
    content = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)
