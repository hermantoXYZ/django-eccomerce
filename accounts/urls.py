from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='index'),
    path('products/', views.product_list, name='product_list'),
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),
    path('orders/', views.order_list, name='order_list'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('order/create/', views.order_create, name='order_create'),
    # Tambahkan pola URL lainnya di sini
    path('page/<slug:slug>/', views.page_detail, name='page_detail'),
]
