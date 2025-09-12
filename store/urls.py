from django.urls import path
from . import views
from .health import health_check, readiness_check

app_name = 'store'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('checkout/', views.checkout, name='checkout'),
    path('order/<str:order_id>/', views.order_detail, name='order_detail'),
    path('orders/', views.order_history, name='order_history'),
    # Health check endpoints
    path('health/', health_check, name='health_check'),
    path('ready/', readiness_check, name='readiness_check'),
]