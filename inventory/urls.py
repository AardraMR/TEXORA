from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('products/', views.products, name='products'),
    path('addproduct/', views.addproduct, name='addproduct'),
    path('deleteproduct/<str:sku_code>/', views.deleteproduct, name='deleteproduct')
]