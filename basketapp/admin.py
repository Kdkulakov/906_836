from django.contrib import admin
from basketapp.models import Basket
# Register your models here.
# admin.site.register(Basket)


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ('product','quantity')
    fields = (('product','quantity'),)
    readonly_fields = ('product',)
    ordering = ('product',)
    search_fields = ('product',)