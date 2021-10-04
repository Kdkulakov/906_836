from random import randrange

from django.core.management import BaseCommand
from faker import Faker

from mainapp.models import Product, ProductCategory


class Command(BaseCommand):
    def handle(self, *args, **options):
        for i in range(100):
            fake = Faker()
            prod = Product()
            prod.name = str(fake.name())
            prod.image = 'products_images/Adidas-hoodie.png'
            prod.description = str(fake.text())
            prod.price = int(randrange(10000))
            prod.quantity = int(randrange(100))
            prod.category = ProductCategory.objects.filter(pk=1)[0]
            prod.save()