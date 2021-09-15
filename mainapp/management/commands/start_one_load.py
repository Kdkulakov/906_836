import os
import json
from mainapp.models import ProductCategory,Product
from django.core.management.base import BaseCommand

class Command(BaseCommand):

        a = [
            {'name': 'Новинки', 'description': 'Новая одежда'},
            {'name': 'Одежда', 'description': 'Новая одежда'},
            {'name': 'Обувь', 'description': 'Новая одежда'},
            {'name': 'Аксессуары', 'description': 'Новая одежда'},
            {'name': 'Подарки', 'description': 'Новая одежда'},
        ]
        for i in a:
            ProductCategory.objects.create(name=i['name'] , description = i['description'])


        BASE_DIR = os.path.abspath(os.curdir)
        print(BASE_DIR)
        c = os.path.join(BASE_DIR, 'mainapp/fixtures/products.json')
        print(c)
        with open(c, 'r', encoding='utf8') as json_file:
            products = json.load(json_file)

        id = ProductCategory.objects.get(name='Новинки')
        for i in products:
            Product.objects.create(name=i['name'], short_description=i['info'],price=i['price'], quantity = 10, status_buy= i['status'],image = i['way'],category_id = id.id)



        def handle(self, *args, **options):
            import this