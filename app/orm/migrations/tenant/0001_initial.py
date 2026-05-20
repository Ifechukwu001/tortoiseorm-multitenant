from tortoise import migrations
from tortoise.migrations import operations as ops
from tortoise.fields.base import OnDelete
from tortoise import fields

class Migration(migrations.Migration):
    initial = True

    operations = [
        ops.CreateModel(
            name='User',
            fields=[
                ('id', fields.BigIntField(generated=True, primary_key=True, unique=True, db_index=True)),
                ('name', fields.CharField(max_length=255)),
                ('email', fields.CharField(unique=True, max_length=255)),
                ('password', fields.CharField(max_length=255)),
            ],
            options={'table': 'user', 'app': 'tenant', 'pk_attr': 'id'},
            bases=['Model'],
        ),
        ops.CreateModel(
            name='Blog',
            fields=[
                ('id', fields.BigIntField(generated=True, primary_key=True, unique=True, db_index=True)),
                ('user', fields.ForeignKeyField('tenant.User', source_field='user_id', db_constraint=True, to_field='id', related_name='blogs', on_delete=OnDelete.CASCADE)),
                ('title', fields.CharField(max_length=255)),
                ('content', fields.TextField(unique=False)),
                ('created_at', fields.DatetimeField(auto_now=False, auto_now_add=True)),
            ],
            options={'table': 'blog', 'app': 'tenant', 'pk_attr': 'id'},
            bases=['Model'],
        ),
    ]
