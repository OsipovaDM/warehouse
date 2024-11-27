from django.db import models
from django.utils import timezone
from django.core.validators import (
    RegexValidator, MaxValueValidator, MinValueValidator, ValidationError
)
from django.db.models import Q


class Tariffs(models.Model):
    title = models.CharField(
        'Название',
        max_length=9,
        unique=True,
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
        help_text='Целое положительное число',
    )
    cost = models.DecimalField(
        'Стоимость',
        max_digits=10,
        decimal_places=2,
        default=0.00,
        help_text='',
    )

    class Meta:
        verbose_name = 'тариф'
        verbose_name_plural = 'Тарифы'
        ordering = ('size_cell', 'period')

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
            ],
        help_text='Формат А0',
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
        ordering = ('number',)

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
        help_text='Формат *@mpei.ru',
    )

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'Клиенты'
        ordering = ('-id',)

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
        verbose_name='Тариф',
        help_text='Размер ячейки должен соответствовать выбранному тарифу',
    )
    duration = models.PositiveIntegerField(
        'Длительность (дни)',
        default=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(365)
        ],
        help_text='Кратно длительности тарифа',
    )
    enumeration = models.TextField(
        'Перепись содержимого',
        blank=True,
        null=True,
        help_text='Необязательное поле',
    )
    prise = models.DecimalField(
        'Расчетная цена',
        max_digits=10,
        decimal_places=2,
        blank=True,
        help_text='Рассчитывается автоматически',
    )
    start = models.DateField(
        'Дата создания',
        default=timezone.now,
        help_text='Важно, чтобы ячейка была свободна на выбранный период времени',
    )
    end = models.DateField(
        'Дата завершения',
        blank=True,
        default=timezone.now,
        help_text='Рассчитывается автоматически',
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

        if self.tariff and self.cell:
            if self.tariff.size_cell != self.cell.size:
                raise ValidationError(f"Размер {self.cell.size} ячейки {self.cell.number} не соответствует заявленному {self.tariff.size_cell} в тарифе {self.tariff.title}")

        existing_orders = Orders.objects.filter(cell=self.cell).filter(Q(end__gt=self.start, end__lt=self.end) | Q(start__gt=self.start, start__lt=self.end) | Q(start__lt=self.start, end__gt=self.end)).values('start', 'end')
        if existing_orders:
            raise ValidationError(f"У выбранной ячейки {self.cell.number} на заданную дату есть активный заказ, {existing_orders}")

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'Заказы'
        ordering = ('-start',)

    def __str__(self):
        return self.cell.number + ' -- ' + self.start.strftime('%d-%m-%Y')
