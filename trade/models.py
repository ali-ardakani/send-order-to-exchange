from django.db import models
from user.models import Account
from django.contrib.auth.models import User

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coin = models.ForeignKey('cryptocurrency.Coin', on_delete=models.CASCADE)
    quantity = models.FloatField()
    send_to_exchange = models.BooleanField(default=False)
    fill = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)