from django.contrib import admin
from .models import Cart, CartItem

# Register your models here.
# admin.site.register(Cart)

class CartItemInline(admin.TabularInline):
    model = CartItem
    raw_id_fields = ['product']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user']
    # list_filter = ['paid', 'created', 'updated']
    inlines = [CartItemInline]
