from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.OrdersCreateView.as_view(), name='create'),
    path('list/', views.OrdersListView.as_view(), name='list'),
    path('<int:pk>/', views.OrdersDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.OrdersUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', views.OrdersDeleteView.as_view(), name='delete'),
]
