from django.contrib import admin
from .models import Product, Store

# Register your models here.


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price',
                    'available', 'created', 'updated','brand', 'sku_size',]
    list_filter = ['available', 'created', 'updated','brand']
    list_editable = ['price', 'available']
    # prepopulated_fields = {'slug': ('name',)}

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'location_area']
    prepopulated_fields = {'slug': ('name',)}


# class ProductInline(admin.TabularInline):
#     model = Product
#     # raw_id_fields = ['product']
#
# @admin.register(Store)
# class StoreAdmin(admin.ModelAdmin):
#     list_display = ['id', 'name', 'slug', 'location_area']
#     # list_filter = ['paid', 'created', 'updated']
#     inlines = [ProductInline]
