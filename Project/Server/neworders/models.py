from django.db import models
from django.conf import settings
import uuid

# Models of the app are included here

from products.models import Product
from billingprofile.models import BillingProfile


ORDER_STATUS_CHOICES =(
        ('created', 'created'),
        ('edited', 'edited'),
        ('cancelled', 'cancelled'),
        ('confirmed', 'confirmed'),
        ('dispatched', 'dispatched'),
        ('delivered', 'delivered')
)

class Order(models.Model):
    # order_id = models.UUIDField(primary_key=True, editable = False, default=uuid.uuid4)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    billingprofile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    order_status = models.CharField(max_length=120, default="Created", choices=ORDER_STATUS_CHOICES)

    #Razorpay fields
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=100, blank=True, null=True)

    #
    class Meta:
        ordering = ('-created',)
    def __str__(self):
        return f'Order {self.id}'
    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                related_name='order_items',
                                on_delete=models.CASCADE)
    # price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    def __str__(self):
        return str(self.id)
    # def get_cost(self):
    #     return self.price * self.quantity
