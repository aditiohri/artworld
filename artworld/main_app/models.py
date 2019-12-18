from django.db import models

# Create your models here.

class Art(models.model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    year = models.IntegerField()
    price = models.IntegerField()
    artist = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.title} {self.artist}"

class Customer(models.model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Order(models.model):
    customer = models.ForeignKey(Customer, on_delete=CASCADE)
    art = models.ForeignKey(Art, on_delete=CASCADE)
    address = models.CharField(max_length=100)
    def __str__(self):
        return self.customer

class Card(models.model):
    name = models.CharField(max_length=100)
    number = models.IntegerField()
    expiry = models.DateField()
    cvv = models.IntergerField()
    billAddress = models.CharField(max_length=100)

    def __str__(self):
        return self.name