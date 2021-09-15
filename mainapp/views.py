from django.shortcuts import render
from django.core.paginator import Paginator

from mainapp.models import  ProductCategory,Product

# функцияя = вьюхи = контролеры.
def index(request):
    context = {
        'title': 'GeekShop',
        'header': 'Добро пожаловать',
        'username': 'Иванов Иван',
    }
    return render(request, 'mainapp/index.html', context)


def products(request,category_id=None,page=1):

    context = {
        'title': 'GeeKshop',
        'header': 'Каталог',
        'menu': ProductCategory.objects.all(),
        'carousel': [
            {'name': 'First slide', 'way': 'slide-1.jpg', 'starter': True},
            {'name': 'Second slide', 'way': 'slide-2.jpg'},
            {'name': 'Third slide', 'way': 'slide-3.jpg'},
        ],
        # 'product': Product.objects.all()

    }
    if category_id:
        products = Product.objects.filter(category_id = category_id).order_by('name')
    else:
        products = Product.objects.all().order_by('name')
    paginator = Paginator(products, per_page=3)
    products_paginator = paginator.page(page)
    context.update({'product':products_paginator})
    return render(request, 'mainapp/products.html', context)


#
