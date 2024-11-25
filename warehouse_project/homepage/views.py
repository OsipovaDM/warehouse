from datetime import datetime, timedelta
from django.db.models import Count, Sum
from django.shortcuts import render
import psycopg2

from storage.models import Orders, Clients


def get_client_count():
    connection = psycopg2.connect(
        host="localhost",
        database="warehouse",
        user="postgres",
        password="sua077m"
    )
    cursor = connection.cursor()
    cursor.execute("SELECT all_clients();")
    result = cursor.fetchone()
    connection.close()
    if result:
        return result[0]
    else:
        return None


def index(request):
    client_count = get_client_count()
    template_name = 'homepage/index.html'
    today = datetime.now().date()
    thirty_days_ago = today - timedelta(days=30)
    context = {
        'client_count': client_count,
    }
    all_orders = Orders.objects.all().select_related('tariff')
    if all_orders:
        context = context | {
            'client_count': client_count,
            'all_orders': all_orders.count(),
            'all_tariff': all_orders.values('tariff__title').annotate(count=Count('id')).order_by('-count')[0]['tariff__title'],
            'all_size': all_orders.values('tariff__size_cell').annotate(count=Count('id')).order_by('-count')[0]['tariff__size_cell'],
            'all_period_mn': 1,
            'all_period_mx': 1,
            'all_cost': all_orders.aggregate(Sum('prise'))['prise__sum'],
        }
    last_orders = all_orders.filter(start__gte=thirty_days_ago)
    if last_orders:
        context = context | {
            'last_orders': last_orders.count(),
            'last_tariff': last_orders.values('tariff__title').annotate(count=Count('id')).order_by('-count')[0]['tariff__title'],
            'last_size': last_orders.values('tariff__size_cell').annotate(count=Count('id')).order_by('-count')[0]['tariff__size_cell'],
            'last_period_mn': 1,
            'last_period_mx': 1,
            'last_cost': last_orders.aggregate(Sum('prise'))['prise__sum'],
        }
    return render(request, template_name, context)
