from django.urls import path
from .views import *

urlpatterns = [
    path('categories/', CategoryListView.as_view()),
    path('categories/<int:id>/', CategoryDetailView.as_view()),
    path('products/', ProductListView.as_view()),
    path('products/<int:id>/', ProductDetailView.as_view()),
    path('cart/', CartView.as_view()),
    path('cart/add/', AddToCartView.as_view()),
    path('cart/remove/', RemoveFromCartView.as_view()),
    path('orders/', MyOrdersView.as_view()),
    path('orders/place/', PlaceOrderView.as_view()),
]
