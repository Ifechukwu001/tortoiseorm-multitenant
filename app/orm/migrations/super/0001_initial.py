from tortoise import migrations
from tortoise.migrations import operations as ops
from tortoise import fields

class Migration(migrations.Migration):
    initial = True

    operations = [
        ops.CreateModel(
            name='PlatformAdmin',
            fields=[
                ('id', fields.BigIntField(generated=True, primary_key=True, unique=True, db_index=True)),
                ('name', fields.CharField(max_length=255)),
                ('email', fields.CharField(unique=True, max_length=255)),
                ('password', fields.CharField(max_length=255)),
            ],
            options={'table': 'platformadmin', 'app': 'super', 'pk_attr': 'id'},
            bases=['Model'],
        ),
        ops.CreateModel(
            name='Tenant',
            fields=[
                ('id', fields.BigIntField(generated=True, primary_key=True, unique=True, db_index=True)),
                ('name', fields.CharField(max_length=255)),
                ('schema', fields.CharField(unique=True, max_length=255)),
            ],
            options={'table': 'tenant', 'app': 'super', 'pk_attr': 'id'},
            bases=['Model'],
        ),
    ]
