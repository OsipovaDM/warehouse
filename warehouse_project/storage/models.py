from django.db import models
from django.utils import timezone
from django.core.validators import (
    RegexValidator, MaxValueValidator, MinValueValidator, ValidationError
)
from django.db.models import Func


class Tariffs(models.Model):
    title = models.CharField(
        'Название',
        max_length=9,
        unique=True
    )
    size_cell = models.CharField(
        'Размер ячейки',
        max_length=6,
        default='Small',
        choices=[
            ('Small', 'Small'),
            ('Medium', 'Medium'),
            ('Large', 'Large'),
        ],
    )
    period = models.PositiveIntegerField(
        'Период (дни)',
        default=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(365)
        ],
    )
    cost = models.DecimalField(
        'Стоимость',
        max_digits=10,
        decimal_places=2,
        default=0.00
    )

    class Meta:
        verbose_name = 'тариф'
        verbose_name_plural = 'Тарифы'

    def __str__(self):
        return self.title


class Cells(models.Model):
    number = models.CharField(
        'Номер',
        max_length=2,
        unique=True,
        validators=[
            RegexValidator(
                regex='^[A-Z][0-9]$',
                message='Первый символ должен быть заглавной латинской буквой, второй - цифрой'
                )
            ]
    )
    size = models.CharField(
        'Размер',
        max_length=6,
        default='Small',
        choices=[
            ('Small', 'Small'),
            ('Medium', 'Medium'),
            ('Large', 'Large'),
        ],
    )

    class Meta:
        verbose_name = 'ячейка'
        verbose_name_plural = 'Ячейки'

    def __str__(self):
        return self.number


class Clients(models.Model):
    FIO = models.CharField(
        'ФИО',
        max_length=255,
        default='Иванов Иван Иванович',
    )
    email = models.EmailField(
        'Почта',
        unique=True,
        null=True,
    )

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return self.FIO


class Orders(models.Model):
    client = models.ForeignKey(
        Clients,
        models.SET_NULL,
        null=True,
        verbose_name='Клиент'
    )
    cell = models.ForeignKey(
        Cells,
        models.SET_NULL,
        null=True,
        verbose_name='Ячейка'
    )
    tariff = models.ForeignKey(
        Tariffs,
        models.SET_NULL,
        null=True,
        verbose_name='Тариф'
    )
    duration = models.PositiveIntegerField(
        'Длительность (дни)',
        default=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(365)
        ],
    )
    enumeration = models.TextField(
        'Перепись содержимого',
        blank=True,
        null=True,
    )
    prise = models.DecimalField(
        'Расчетная цена',
        max_digits=10,
        decimal_places=2,
        blank=True,
    )
    start = models.DateField(
        'Дата создания',
        default=timezone.now
    )
    end = models.DateField(
        'Дата завершения',
        blank=True,
        default=timezone.now
    )

    def save(self, *args, **kwargs):
        if self.start and self.duration:
            self.end = self.start + timezone.timedelta(days=self.duration-1)
        if self.tariff and self.duration:
            self.prise = self.tariff.cost * self.duration
        super().save(*args, **kwargs)

    def clean(self):
        super().clean()

        if self.tariff and self.duration:
            tariff_period = self.tariff.period
            if self.duration % tariff_period != 0:
                raise ValidationError(f"Длительность должна быть кратна {tariff_period} дням")

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return self.cell.number + ' -- ' + self.start.strftime('%d-%m-%Y')
