from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from cryptocurrency.models import Coin
from trade.models import Order
from .models import Account

class TradeTestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='testuser1', password='12345')
        self.user2 = User.objects.create_user(username='testuser2', password='12345')
        Account.objects.all().update(balance=100)
        self.coin = Coin.objects.create(name='aban', symbol='ABAN', price=4)
    
    def test_order(self):
        self.client.login(username='testuser1', password='12345')
        response = self.client.post('/order/', {'symbol': 'ABAN', 'quantity': 10})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['symbol'], 'ABAN')
        self.assertEqual(response.data['quantity'], 10)
        self.assertEqual(Account.objects.get(user=self.user1).balance, 60)
        self.assertEqual(Order.objects.filter(user=self.user1).count(), 1)
        
    def test_insufficient_balance(self):
        self.client.login(username='testuser1', password='12345')
        response = self.client.post('/order/', {'symbol': 'ABAN', 'quantity': 101})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data[0], 'Insufficient balance')
        self.assertEqual(Account.objects.get(user=self.user1).balance, 100)
        self.assertEqual(Order.objects.filter(user=self.user1).count(), 0)
        
    def test_coin_does_not_exist(self):
        self.client.login(username='testuser1', password='12345')
        response = self.client.post('/order/', {'symbol': 'ABAN1', 'quantity': 10})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['non_field_errors'][0], 'Coin does not exist')
        self.assertEqual(Account.objects.get(user=self.user1).balance, 100)
        self.assertEqual(Order.objects.filter(user=self.user1).count(), 0)
        
    def test_send_order_to_exchange(self):
        self.client.login(username='testuser1', password='12345')
        response = self.client.post('/order/', {'symbol': 'ABAN', 'quantity': 25})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['symbol'], 'ABAN')
        self.assertEqual(response.data['quantity'], 25)
        self.assertEqual(Account.objects.get(user=self.user1).balance, 0)
        self.assertEqual(Order.objects.filter(user=self.user1).count(), 1)
        self.assertEqual(Order.objects.get(user=self.user1).send_to_exchange, True)
        
    def test_send_order_to_exchange_cumulative(self):
        self.client.login(username='testuser1', password='12345')
        response = self.client.post('/order/', {'symbol': 'ABAN', 'quantity': 2})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.get(user=self.user1).send_to_exchange, False)
        self.client.logout()
        self.client.login(username='testuser2', password='12345')
        response = self.client.post('/order/', {'symbol': 'ABAN', 'quantity': 1})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.get(user=self.user2).send_to_exchange, True)
        self.assertEqual(Order.objects.get(user=self.user1).send_to_exchange, True)
        
        