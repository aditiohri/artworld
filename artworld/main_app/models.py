from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


# Create your models here.

class Art(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    year = models.IntegerField()
    price = models.IntegerField()
    artist = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.title} {self.artist}"
    
class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    
    def __str__(self):
        return self.name

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    art = models.ForeignKey(Art, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    def __str__(self):
        return self.customer

class Card(models.Model):
    name = models.CharField(max_length=100)
    number = models.IntegerField()
    expiry = models.DateField()
    cvv = models.IntegerField()
    billAddress = models.CharField(max_length=100)

    def __str__(self):
        return self.name