from tortoise.models import Model
from tortoise import fields


class Product(Model):
    id = fields.BigIntField(pk=True, null=False, index=True, unique=True)
    name = fields.TextField()
    cost = fields.IntField(null=False)
    image = fields.TextField(null=True)


