from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings

# Create your models here.

class Art(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    year = models.IntegerField()
    price = models.IntegerField()
    artist = models.CharField(max_length=100)
    image = models.ImageField()

    def __str__(self):
        return f"{self.title} {self.artist}"

class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    art = models.ForeignKey(Art, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.art

    def get_total_item_price(self):
        return self.item.price

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem)
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

    def get_total(self):
        total = 0
        for cart_item in self.items.all():
            total += cart_item.get_final_price()
        return total


    
class Card(models.Model):
    name = models.CharField(max_length=100)
    number = models.IntegerField()
    expiry = models.DateField()
    cvv = models.IntegerField()
    billAddress = models.CharField(max_length=100)

    def __str__(self):
        return self.name