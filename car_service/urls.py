from django.urls import path, include
from . import views

urlpatterns = [
    path('index/', views.index, name="index"),
    path('cars/', views.cars, name='cars'),
    path('car/<int:pk>/', views.car_detail, name='car_detail'),
    path('orders/', views.OrderListView.as_view(), name='orders'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('search/', views.search_results, name='search_results'),
    path('', views.index, name='index'),

    path('myorders/', views.ServiceOrderByUserListView.as_view(), name="current-orders"),
    path('register/', views.register_user, name="register-url"),
]

