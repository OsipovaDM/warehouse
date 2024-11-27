from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)
from django.urls import reverse_lazy

from storage.models import Cells, Tariffs, Orders, Clients


class OrdersMixin:
    model = Orders
    success_url = reverse_lazy('orders:list')


class OrdersCreateView(OrdersMixin, CreateView):
    # form_class = OrdersForm
    fields = 'client', 'cell', 'tariff', 'duration', 'enumeration', 'start'
    pass


class OrdersDetailView(DetailView):
    model = Orders

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        my_order = self.object
        context['cell'] = my_order.cell
        context['tariff'] = my_order.tariff
        context['client'] = my_order.client
        return context


class OrdersUpdateView(OrdersMixin, UpdateView):
    # form_class = OrdersForm
    fields = 'client', 'cell', 'tariff', 'duration', 'enumeration', 'start'
    pass


class OrdersDeleteView(OrdersMixin, DeleteView):
    template_name = 'storage/orders_form.html'
    pass


class OrdersListView(ListView):
    model = Orders
    # ordering = 'id'
    # paginate_by = 10
