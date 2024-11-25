from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)
from django.urls import reverse_lazy

from storage.models import Cells, Tariffs, Orders, Clients


class CellsMixin:
    model = Cells
    success_url = reverse_lazy('cells:list')


class CellsCreateView(CellsMixin, CreateView):
    # form_class = CellsForm
    fields = '__all__'
    pass


class CellsDetailView(DetailView):
    model = Cells

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        my_cell = self.object
        my_order = Orders.objects.select_related('tariff').select_related('client').filter(cell=my_cell).order_by('-end').first()
        context['order'] = my_order
        return context


class CellsUpdateView(CellsMixin, UpdateView):
    # form_class = CellsForm
    fields = '__all__'
    pass


class CellsDeleteView(CellsMixin, DeleteView):
    template_name = 'storage/cells_form.html'
    pass


class CellsListView(ListView):
    model = Cells
    ordering = 'id'
    # paginate_by = 10
