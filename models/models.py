from tortoise.models import Model
from tortoise import fields

class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=100)
    email = fields.CharField(max_length=100, unique=True)
    password = fields.CharField(max_length=100)

    class Meta:
        table = "users"

class Product(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100)
    category = fields.CharField(max_length=50)
    description = fields.TextField()
    image_url = fields.CharField(max_length=200, null=True)

    class Meta:
        table = "products"