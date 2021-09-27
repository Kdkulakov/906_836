from django.db import models


class ProductCategory(models.Model):
    description = models.TextField(blank=True)
    name = models.CharField(max_length=128, unique=True)

    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Product Categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField(blank=True)
    short_description = models.CharField(max_length=128, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products_images', blank=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)  # PROTECT
    status_buy = models.CharField(max_length=64, default='Отправить в корзину')

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    @staticmethod
    def get_items():
        return Product.objects.filter(is_active=True).order_by('category', 'name')
