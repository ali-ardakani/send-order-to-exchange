from django.db.models.signals import post_save, pre_save
from trade.models import Order
from django.dispatch import receiver
from django.db import models
from .commands import buy_from_exchange


@receiver(pre_save, sender=Order)
def update_balance(sender, instance, **kwargs):
    if instance.user.account.balance >= instance.coin.price * instance.quantity:
        instance.user.account.balance -= instance.coin.price * instance.quantity
        instance.user.account.save()
    else:
        raise ValueError('Insufficient balance')

@receiver(post_save, sender=Order)
def minimum_send(sender, instance, created, **kwargs):
    """
    send order to exchange when amount of order is greater than 10$
    """
    orders = Order.objects.filter(send_to_exchange=False, coin=instance.coin)
    total = orders.values('coin').aggregate(
    total=models.Sum(models.F('quantity') * models.F('coin__price'),
                        output_field=models.FloatField(),
                        default=0.0))
    if total['total'] >= 10:
        orders.update(send_to_exchange=True)
        # send to exchange
        buy_from_exchange(symbol=instance.coin.symbol, quantity=total['total'])