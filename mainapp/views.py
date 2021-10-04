from django.shortcuts import render
from django.core.paginator import Paginator

from mainapp.models import ProductCategory, Product
from django.conf import settings
from django.core.cache import cache
from django.views.decorators.cache import cache_page


def get_links_menu():
    if settings.LOW_CACHE:
        key = 'links_menu'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ProductCategory.objects.all()
            cache.set(key, links_menu)
        return links_menu
    else:
        return ProductCategory.objects.all()


def get_products():
    if settings.LOW_CACHE:
        key = 'products'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True, category__is_active=True).select_related('category')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True, category__is_active=True).select_related('category')


# функцияя = вьюхи = контролеры.
def index(request):
    context = {
        'title': 'GeekShop',
        'header': 'Добро пожаловать',
        'username': 'Иванов Иван',
    }
    return render(request, 'mainapp/index.html', context)


def products(request, category_id=None, page=1):
    context = {
        'title': 'GeeKshop',
        'header': 'Каталог',
        'menu': get_links_menu(),
        'carousel': [
            {'name': 'First slide', 'way': 'slide-1.jpg', 'starter': True},
            {'name': 'Second slide', 'way': 'slide-2.jpg'},
            {'name': 'Third slide', 'way': 'slide-3.jpg'},
        ],
        # 'product': Product.objects.all()

    }
    if category_id:
        products = Product.objects.filter(category_id=category_id).order_by('name')
    else:
        products = get_products()
    paginator = Paginator(products, per_page=3)
    products_paginator = paginator.page(page)
    context.update({'product': products_paginator})
    return render(request, 'mainapp/products.html', context)

#
