from django.contrib import admin
from authapp.models import User
# Register your models here.
# admin.site.register(User)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username','first_name','last_name','email','is_active','is_staff')
    # readonly_fields = ('username','first_name','last_name','email','is_active','staff_status')
    ordering = ('username',)
    search_fields = ('username','email')