from django.db import models

# Create your models here.

class Art(models.model):
    title = models.charField(max_length=100)
    description = models.TextField(max_length=250)
    year = models.IntegerField()
    price = models.IntegerField()
    artist = models.charField(max_length=100)

    def __str__(self):
        return f"{self.title} {self.artist}"