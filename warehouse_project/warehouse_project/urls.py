"""warehouse_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # Приложение для работы с админ зоной
    path('admin/', admin.site.urls),
    # Приложения для работы с пользователями
    path('auth/', include('django.contrib.auth.urls')),
    # Приложение для главной страницы
    path('', include('homepage.urls')),
    # Приложение для работы с ячейками
    path('cells/', include('cells.urls')),
    # Приложение для работы с клиентами
    path('clients/', include('clients.urls')),
    # Приложение для работы с пользователями
    path('orders/', include('orders.urls')),
    # Приложение для работы с тарифами
    path('tariffs/', include('tariffs.urls')),
]
