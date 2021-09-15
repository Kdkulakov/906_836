from django.contrib import admin

# Register your models here.
from mainapp.models import ProductCategory,Product
# admin.site.register(Product)
# admin.site.register(ProductCategory)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','price','quantity','category')
    fields = ('name','image','description','short_description',('price','quantity'),'category')
    readonly_fields = ('short_description',)
    ordering = ('name',)
    search_fields = ('name',)

@admin.register(ProductCategory)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','description')
    ordering = ('name',)
    search_fields = ('name',)
