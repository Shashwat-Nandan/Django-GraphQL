from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    email = models.EmailField(unique=True, max_length=255)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # removes email from REQUIRED_FIELDS

    class Kinds(models.TextChoices):
        RETAILER = "RETAILER", 'Retailer'
        CUSTOMER = "CUSTOMER", 'Customer'

    kind = models.CharField(_('Kind'), max_length=50, choices=Kinds.choices, default=Kinds.RETAILER)

    name = models.CharField(_('Name of User'), blank=True, max_length=255)

    # def get_absolute_url(self):
    #     return reverse("users:detail", kwargs={"username":self.username})

class RetailerManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(kind= User.Kinds.RETAILER)

class CustomerManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(kind= User.Kinds.CUSTOMER)

class Retailer(User):
    objects = RetailerManager()
    class Meta:
        proxy=True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.kind= User.Kinds.RETAILER
        return super().save(*args, **kwargs)

class Customer(User):
    objects = CustomerManager()
    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.kind= User.Kinds.CUSTOMER
        return super().save(*args, **kwargs)
