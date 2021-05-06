from rest_framework import serializers
from .models import Product, Store

class StoreSerializer(serializers.ModelSerializer):
        class Meta:
            model = Store
            fields = ('user', 'name', 'slug', 'location_area', 'pin_code')


class ProductSerializer(serializers.ModelSerializer):
        class Meta:
            model = Product
            fields = ('store', 'name', 'brand', 'sku_size', 'slug', 'image', 'description', 'price', 'available', 'created', 'updated')
