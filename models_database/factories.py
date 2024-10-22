import factory
from factory.django import ImageField
from models_database import models
from models_database.models import Category


class CategoryFactory(factory.django.DjangoModelFactory):
    category_name = factory.Faker('word')
    description = factory.Faker('text')

    class Meta:
        model = models.Category


class ProductFactory(factory.django.DjangoModelFactory):
    product_name = factory.Faker('word')
    description = factory.Faker('text')
    price = factory.Faker('random_int', min=0, max=1000)
    quantity = factory.Faker('random_int', min=0, max=500)
    image = factory.Faker('image_url')
    category = factory.SubFactory(CategoryFactory)

    class Meta:
        model = models.Product
