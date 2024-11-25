from django.urls import path
from . import views

app_name = 'clients'

urlpatterns = [
    path('', views.client, name='create'),
    path('list/', views.list, name='list'),
    path('<int:pk>/detail/', views.detail, name='detail'),
    path('<int:pk>/edit/', views.client, name='edit'),
    path('<int:pk>/delete/', views.delete_client, name='delete'),
]
