from django.urls import path
from . import views

app_name = 'tariffs'

urlpatterns = [
    path('', views.TariffsCreateView.as_view(), name='create'),
    path('list/', views.TariffsListView.as_view(), name='list'),
    path('<int:pk>/', views.TariffsDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.TariffsUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', views.TariffsDeleteView.as_view(), name='delete'),
]
