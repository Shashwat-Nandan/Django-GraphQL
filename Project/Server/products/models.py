from django.db import models
from django.urls import reverse
from django.conf import settings

# Create your models here.

class Store(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    name = models.CharField(max_length=200,
                            db_index=True)
    slug = models.SlugField(max_length=200,
                            blank=True )
    location_area = models.CharField(max_length=200, db_index=True)
    pin_code = models.IntegerField()
    class Meta:
        ordering = ('name',)
        verbose_name = 'store'
        verbose_name_plural = 'stores'
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('productlist_by_store',
                       args=[self.slug])


class Product(models.Model):
    store = models.ForeignKey(Store,on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)

    brand = models.CharField(max_length=100, db_index=True)
    sku_size = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200,blank=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d',
                              blank=True)
    description = models.TextField(blank=True)
    # price = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.FloatField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)
    def __str__(self):
        return self.name
    # def get_absolute_url(self):
    #     return reverse('product_detail',
    #                    args=[self.id, self.slug])
