# Generated by Django 3.2.16 on 2024-11-18 12:18

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0002_auto_20241118_1334'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orders',
            old_name='start_date',
            new_name='start',
        ),
        migrations.RemoveField(
            model_name='orders',
            name='end_date',
        ),
        migrations.AddField(
            model_name='orders',
            name='end',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, verbose_name='Дата завершения'),
        ),
        migrations.AlterField(
            model_name='orders',
            name='enumeration',
            field=models.TextField(blank=True, null=True, verbose_name='Перепись содержимого'),
        ),
        migrations.AlterField(
            model_name='orders',
            name='prise',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, verbose_name='Расчетная цена'),
        ),
    ]