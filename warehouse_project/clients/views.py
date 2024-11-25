import psycopg2
from django.shortcuts import get_object_or_404, render, redirect

from .forms import ClientsForm
from storage.models import Clients


def detail(request, pk=None):
    connection = psycopg2.connect(
        host="localhost",
        database="warehouse",
        user="postgres",
        password="sua077m"
    )
    cursor = connection.cursor()
    cursor.execute(f'SELECT c.id, c."FIO", c.email FROM storage_clients c WHERE id = {pk};')
    results = cursor.fetchall()
    column_names = [description[0] for description in cursor.description]
    client = [{column: value for column, value in zip(column_names, row)} for row in results][0]
    connection.close()

    context = {'client': client}
    template_name = 'clients/clients_detail.html'
    return render(request, template_name, context)


def client(request, pk=None):
    if pk is not None:
        instance = get_object_or_404(Clients, pk=pk)
    else:
        instance = None
    form = ClientsForm(request.POST or None, instance=instance)
    context = {'form': form}
    if form.is_valid():
        fio = form.cleaned_data['FIO']
        email = form.cleaned_data['email']
        # form.save()  # Здесь должен быть вызов функции из БД
        connection = psycopg2.connect(
            host="localhost",
            database="warehouse",
            user="postgres",
            password="sua077m"
        )
        cursor = connection.cursor()
        cursor.execute(f'CALL update_clients({pk}, \'{fio}\', \'{email}\');')
        connection.commit()
        connection.close()
    return render(request, 'clients/clients_form.html', context)


def delete_client(request, pk):
    instance = get_object_or_404(Clients, pk=pk)
    form = ClientsForm(instance=instance)
    context = {'form': form}
    if request.method == 'POST':
        instance.delete()  # Здесь должен быть вызов функции из БД
        return redirect('clients:list')
    return render(request, 'clients/clients_form.html', context)


def list(request):
    clients_list = Clients.objects.order_by('id')  # Здесь должен быть вызов функции из БД
    context = {'clients_list': clients_list}
    return render(request, 'clients/clients_list.html', context)


def client_RewSQL(request):
    template_name = 'homepage/index.html'
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
        return render(request, template_name, result[0])
    else:
        return render(request, template_name)
