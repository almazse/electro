from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'authentication'

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('user/', views.user_page, name='user'),
    path('admin/', views.admin_page, name='admin'),
    path('admin/top/', views.admin_page_top, name='admin_top'),
    path('admin/products/', views.admin_page_products, name='admin_products'),
    path('admin/add_product/', views.admin_page_add_product, name='admin_add_product'),
    path('signin/', views.sign_in, name='signin')
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)