from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.homepage, name='home'),
    path('store/', views.store, name='store'),
    path('store/<category_slug>/', views.store, name='store'),
    path('checkout/', views.checkout, name='checkout'),
    path('product/<int:pk>', views.product, name='product')
]
