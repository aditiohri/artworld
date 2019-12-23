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

    def __str__(self):
        return f"{self.title} {self.artist}"

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    art = models.ForeignKey(Art, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)

    def __str__(self):
        return self.art
    
class Card(models.Model):
    name = models.CharField(max_length=100)
    number = models.IntegerField()
    expiry = models.DateField()
    cvv = models.IntegerField()
    billAddress = models.CharField(max_length=100)

    def __str__(self):
        return self.name