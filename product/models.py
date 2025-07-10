from tortoise.models import Model
from tortoise import fields

class Product(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=255)
    category = fields.CharField(max_length=100)
    description = fields.TextField()
    image_url = fields.CharField(max_length=255)

    def __str__(self):
        return self.title
