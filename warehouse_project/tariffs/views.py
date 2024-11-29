from datetime import datetime, timedelta
from django.db.models import Count
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)
from django.urls import reverse_lazy

from storage.models import Tariffs, Orders


class TariffsMixin:
    model = Tariffs
    success_url = reverse_lazy('tariffs:list')


class TariffsCreateView(TariffsMixin, CreateView):
    # form_class = TariffsForm
    fields = '__all__'
    pass


class TariffsDetailView(DetailView):
    model = Tariffs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        my_tariff = self.object
        my_orders = Orders.objects.select_related('cells').select_related('client').filter(tariff=my_tariff).order_by('-end')
        today = datetime.now().date()
        thirty_days_ago = today - timedelta(days=30)
        try:
            context['active_orders_count'] = my_orders.values('end').filter(end__gt=today).count()
        except IndexError:
            context['active_orders_count'] = 0
        try:
            context['created_orders_last_month'] = my_orders.values('start').filter(start__gt=thirty_days_ago).count()
        except IndexError:
            context['created_orders_last_month'] = 0
        try:
            context['created_orders_all'] = my_orders.count()
        except IndexError:
            context['created_orders_all'] = 0
        return context


class TariffsUpdateView(TariffsMixin, UpdateView):
    # form_class = TariffsForm
    fields = '__all__'
    pass


class TariffsDeleteView(TariffsMixin, DeleteView):
    template_name = 'storage/tariffs_form.html'
    pass


class TariffsListView(ListView):
    model = Tariffs
    # ordering = 'id'
    # paginate_by = 10
