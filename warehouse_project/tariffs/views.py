from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)
from django.urls import reverse_lazy

from storage.models import Tariffs


class TariffsMixin:
    model = Tariffs
    success_url = reverse_lazy('tariffs:list')


class TariffsCreateView(TariffsMixin, CreateView):
    # form_class = TariffsForm
    pass


class TariffsDetailView(DetailView):
    model = Tariffs


class TariffsUpdateView(TariffsMixin, UpdateView):
    # form_class = TariffsForm
    fields = '__all__'
    pass


class TariffsDeleteView(TariffsMixin, DeleteView):
    pass


class TariffsListView(ListView):
    model = Tariffs
    ordering = 'id'
    paginate_by = 10
