# Generated by Django 3.2.16 on 2024-11-17 14:06

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cells',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=2, unique=True, validators=[django.core.validators.RegexValidator(message='Первый символ должен быть заглавной латинской буквой, второй - цифрой', regex='^[A-Z][0-9]$')], verbose_name='Номер')),
                ('size', models.CharField(choices=[('Small', 'Small'), ('Medium', 'Medium'), ('Large', 'Large')], default='Small', max_length=6, verbose_name='Размер')),
            ],
            options={
                'verbose_name': 'ячейка',
                'verbose_name_plural': 'Ячейки',
            },
        ),
        migrations.CreateModel(
            name='Clients',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('FIO', models.CharField(default='Иванов Иван Иванович', max_length=255, verbose_name='ФИО')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Почта')),
            ],
            options={
                'verbose_name': 'клиент',
                'verbose_name_plural': 'Клиенты',
            },
        ),
        migrations.CreateModel(
            name='Tariffs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=9, unique=True, verbose_name='Название')),
                ('size_cell', models.CharField(choices=[('Small', 'Small'), ('Medium', 'Medium'), ('Large', 'Large')], default='Small', max_length=6, verbose_name='Размер ячейки')),
                ('period', models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(365)], verbose_name='Период (дни)')),
                ('cost', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Стоимость')),
            ],
            options={
                'verbose_name': 'тариф',
                'verbose_name_plural': 'Тарифы',
            },
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('duration', models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(365)], verbose_name='Длительность (дни)')),
                ('enumeration', models.TextField(null=True, verbose_name='Перепись содержимого')),
                ('prise', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Расчетная цена')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('cell', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='storage.cells', verbose_name='Ячейка')),
                ('client', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='storage.clients', verbose_name='Клиент')),
                ('tariff', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='storage.tariffs', verbose_name='Тариф')),
            ],
            options={
                'verbose_name': 'заказ',
                'verbose_name_plural': 'Заказы',
            },
        ),
    ]