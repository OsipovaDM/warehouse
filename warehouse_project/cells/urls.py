from django.urls import path
from . import views

app_name = 'cells'

urlpatterns = [
    path('', views.CellsCreateView.as_view(), name='create'),
    path('list/', views.CellsListView.as_view(), name='list'),
    path('<int:pk>/', views.CellsDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.CellsUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', views.CellsDeleteView.as_view(), name='delete'),
]
