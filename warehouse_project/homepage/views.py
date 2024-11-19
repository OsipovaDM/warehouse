from django.shortcuts import render

from storage.models import Orders


def index(request):
    template_name = 'homepage/index.html'
    orders = Orders.objects.all().select_related('tarriff')
    context = {
        'last_orders': 1,
        'last_tariff': 1,
        'last_size': 1,
        'last_period_mn': 1,
        'last_period_mx': 1,
        'last_cost': 1,
        'all_orders': 1,
        'all_tariff': 1,
        'all_size': 1,
        'all_period_mn': 1,
        'all_period_mx': 1,
        'all_cost': 1,
    }
    return render(request, template_name, context)
