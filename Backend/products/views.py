# products/views.py

from django.contrib.auth import get_user_model
from rest_framework import generics, viewsets
from .models import Product, Store
from .serializers import ProductSerializer, StoreSerializer

class ProductViewSet(viewsets.ModelViewSet): # new
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class StoreViewSet(viewsets.ModelViewSet): # new
    queryset = Store.objects.all()
    serializer_class = StoreSerializer











# class ProductList(generics.ListAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#
# # class ProductListByStore(generics.ListAPIView):
# #     queryset = Product.objects.all()
# #     serializer_class = ProductSerializer
#
# class ProductDetails(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
