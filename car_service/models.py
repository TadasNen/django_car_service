from django.db import models
from django.contrib.auth.models import User
from datetime import date
import uuid
from tinymce.models import HTMLField


class CarModel(models.Model):
    brand = models.CharField('Brand', max_length=100)
    model = models.CharField('Model', max_length=100)
    year = models.IntegerField('Year')
    engine = models.CharField('Engine', max_length=100)

    class Meta:
        ordering = ['brand', 'model', ]

    def __str__(self):
        return f'{self.brand} {self.model} | {self.year}'


class Car(models.Model):
    license_plate = models.CharField('License plate', max_length=7)
    vin = models.CharField('VIN', max_length=17)
    client = models.CharField('Client', max_length=100)
    car_model = models.ForeignKey(CarModel, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to='car_images/', null=True, blank=True)
    # description = models.TextField('Description', null=True, blank=True, max_length=300)
    description = HTMLField()

    class Meta:
        ordering = ['client', 'car_model']

    def __str__(self):
        return f'{self.client} {self.car_model}'


class Service(models.Model):
    name = models.CharField('Name', max_length=50)
    price = models.FloatField('Price, EUR')

    class Meta:
        ordering = ['name', ]

    def __str__(self):
        return f'{self.name} {round(self.price)} EUR'


class Order(models.Model):
    date = models.DateField('Date', null=True, blank=True)
    car = models.ForeignKey(Car, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    ORDER_STATUS = (
        ('p', 'Processing'),
        ('o', 'Ordered'),
        ('s', 'In service'),
        ('c', 'Completed'),
        ('t', 'Taken back by customer')
    )
    status = models.CharField(max_length=1, choices=ORDER_STATUS,
                              blank=True, default='p')

    @property
    def order_total_price(self):
        order_rows = self.order_row.all()
        total_price = sum(row.total_price for row in order_rows)
        return round(total_price)

    @property
    def order_rows(self):
        return ', '.join(str(el) for el in self.order_row.all())

    @property
    def is_overdue(self):
        if self.date and date.today() > self.date:
            return True
        else:
            return False

    def __str__(self):
        return f'{self.car}'



class OrderRow(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique service ID', editable=False)
    amount = models.IntegerField('Amount')
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, related_name='service')
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, related_name='order_row')

    @property
    def total_price(self):
        total__for_amount = self.service.price * self.amount
        return total__for_amount

    @property
    def service_name(self):
        return self.service.name

    @property
    def client_car(self):
        return self.order.car

    @property
    def order_date(self):
        return self.order.date

    def __str__(self):
        return f'{self.amount} orders of {self.service.name} for total {self.total_price} EUR'
