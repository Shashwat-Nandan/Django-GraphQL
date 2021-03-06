from django.db import models
from products.models import Product
from users.models import User

# Create your models here.


class CartItem(models.Model):

    cart = models.ForeignKey('Cart', on_delete=models.CASCADE)
    product= models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

class Cart(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through=CartItem)
