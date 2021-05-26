from django.db import models
from django.conf import settings
# Create your models here.

class BillingProfile(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    # address2 = models.CharField(max_length=250)

    def __str__(self):
        return str(self.email)
