from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings
from django_countries.fields import CountryField

# Create your models here.

ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)

class Art(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    year = models.IntegerField()
    price = models.FloatField()
    artist = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.title} {self.artist}"

    class Meta:
        verbose_name_plural = 'Artwork'

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    art = models.ForeignKey(Art, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.art.title} is worth {self.art.price}"

    def get_item_price(self):
        return self.art.price

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    art = models.ManyToManyField(Cart)
    ordered_date = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey(
        'Address', related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    billing_address = models.ForeignKey(
        'Address', related_name='billing_address', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.user.username

    def get_total_price(self):
        total = 0
        for cart_item in self.items.all():
            total += cart_item.get_item_price()
        return total

class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Addresses'

class Payment(models.Model):
    # stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    
class Card(models.Model):
    name = models.CharField(max_length=100)
    number = models.IntegerField()
    expiry = models.DateField()
    cvv = models.IntegerField()
    billAddress = models.CharField(max_length=100)

    def __str__(self):
        return self.name