from django.db import models

class Coin(models.Model):
    name = models.CharField(max_length=50)
    symbol = models.CharField(max_length=50)
    price = models.FloatField()

    def __str__(self):
        return self.name
