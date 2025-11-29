from rest_framework import serializers
from .models import Product, Category, Cart, CartItem, Order, OrderItem

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(source='cartitem_set', many=True)
    class Meta:
        model = Cart
        fields = ['id', 'user', 'cart_items']

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(source='orderitem_set', many=True)
    class Meta:
        model = Order
        fields = ['id', 'user', 'total_amount', 'status', 'created_at', 'order_items']
