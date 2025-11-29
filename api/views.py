from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Product, Category, Cart, CartItem, Order, OrderItem
from .serializers import (
    ProductSerializer, 
    CategorySerializer, 
    CartSerializer, 
    CartItemSerializer,
    OrderSerializer
)

# -------------------------
# CATEGORY
# -------------------------
class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'id'

# -------------------------
# PRODUCT
# -------------------------
class ProductListView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'

# -------------------------
# CART
# -------------------------
class CartView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer

    def get_object(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart

class AddToCartView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartItemSerializer

    def post(self, request):
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))

        cart, _ = Cart.objects.get_or_create(user=request.user)
        product = get_object_or_404(Product, id=product_id)

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        cart_item.quantity += quantity
        cart_item.save()

        return Response({"message": "Item added to cart"}, status=200)

class RemoveFromCartView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        cart = get_object_or_404(Cart, user=request.user)
        product_id = request.data.get("product_id")
        CartItem.objects.filter(cart=cart, product_id=product_id).delete()
        return Response({"message": "Item removed"}, status=200)

# -------------------------
# ORDERS
# -------------------------
class PlaceOrderView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart = get_object_or_404(Cart, user=request.user)
        items = cart.cartitem_set.all()

        if not items:
            return Response({"error": "Cart is empty"}, status=400)

        total = sum(item.product.price * item.quantity for item in items)

        # Create order
        order = Order.objects.create(
            user=request.user,
            total_amount=total,
            status='pending'
        )

        # Move cart items → order items
        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        items.delete()  # clear cart

        return Response({"message": "Order placed", "order_id": order.id}, status=201)

class MyOrdersView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
