from django.urls import path
from . import views

app_name = 'cart'
urlpatterns = [
    path('search/', views.search, name='search'),
    path('', views.cart_detail, name='cart_detail'),
    path('add/<int:product_id>', views.cart_add, name='cart_add'),
    path('remove/<int:product_id>', views.cart_remove, name='cart_remove'),
    path('filter/price/', views.filter_by_price, name='filter_by_price'),
]
