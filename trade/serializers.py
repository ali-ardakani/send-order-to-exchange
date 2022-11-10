from rest_framework import serializers
from .models import Order
from cryptocurrency.models import Coin


class OrderSerializer(serializers.Serializer):
    symbol = serializers.CharField(max_length=50, write_only=True)
    quantity = serializers.FloatField()
    date = serializers.DateTimeField(read_only=True)
        
    def create(self, validated_data):
        user_id = self.context['request'].user.id
        try:
            new_order = Order.objects.create(
                user_id=user_id,
                coin_id=validated_data['coin_id'],
                quantity=validated_data['quantity'],
            )
            return new_order
        except Exception as e:
            raise serializers.ValidationError(str(e), code=400)
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data = {'symbol': instance.coin.symbol, **data}
        return data
    
    def validate(self, attrs):
        coin = Coin.objects.filter(symbol__iexact=attrs['symbol'])
        if coin.exists():
            attrs['coin_id'] = coin.first().id
        else:
            raise serializers.ValidationError("Coin does not exist")
        
        if attrs['quantity'] <= 0:
            raise serializers.ValidationError("Quantity must be greater than 0")
        
        del attrs['symbol']
        return attrs