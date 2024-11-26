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
    cursor.execute(f'''SELECT
                   c.id, c."FIO", c.email,
                   s.number, s.size, s.title, s.duration,
                   s.start, s.end, s.prise, s.enumeration
                   FROM storage_statistics s 
                   JOIN storage_clients c
                   ON c.email = s.email
                   WHERE id = {pk}
                   ORDER BY s.start desc;''')
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
        connection = psycopg2.connect(
            host="localhost",
            database="warehouse",
            user="postgres",
            password="sua077m"
        )
        cursor = connection.cursor()
        if pk is not None:
            cursor.execute(f'CALL update_clients({pk}, \'{fio}\', \'{email}\');')
        else:
            cursor.execute(f'CALL insert_clients(\'{fio}\', \'{email}\');')
        connection.commit()
        connection.close()
    return render(request, 'clients/clients_form.html', context)


def delete_client(request, pk):
    instance = get_object_or_404(Clients, pk=pk)
    form = ClientsForm(instance=instance)
    context = {'form': form}
    if request.method == 'POST':
        connection = psycopg2.connect(
            host="localhost",
            database="warehouse",
            user="postgres",
            password="sua077m"
        )
        cursor = connection.cursor()
        cursor.execute(f'CALL delete_clients({pk});')
        connection.commit()
        connection.close()
        return redirect('clients:list')
    return render(request, 'clients/clients_form.html', context)


def list(request):
    # clients_list = Clients.objects.order_by('id')  # Здесь должен быть вызов функции из БД
    connection = psycopg2.connect(
        host="localhost",
        database="warehouse",
        user="postgres",
        password="sua077m"
    )
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM select_clients();')
    results = cursor.fetchall()
    column_names = [description[0] for description in cursor.description]
    clients_list = [{column: value for column, value in zip(column_names, row)} for row in results]
    connection.close()
    context = {'clients_list': clients_list}
    return render(request, 'clients/clients_list.html', context)