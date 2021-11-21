from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('checkout/', views.cart_checkout, name='cart_checkout'),
    path('remove/<int:product_id>/', views.cart_remove, name='cart_remove')
]