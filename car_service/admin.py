from django.contrib import admin
from .models import CarModel, Car, Order, OrderRow, Service


class CarModelAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model', 'year', 'engine')
    search_fields = ('brand', 'model', 'year')


class CarAdmin(admin.ModelAdmin):
    list_display = ('client', 'car_model', 'license_plate', 'vin')
    search_fields = ('client', 'car_model', 'license_plate', 'vin')

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    list_editable = ('price', )
    search_fields = ('name', )

class OrderRowInline(admin.TabularInline):
    model = OrderRow
    extra = 1

class OrderRowAdmin(admin.ModelAdmin):
    list_display = ('client_car', 'service_name', 'amount','total_price', 'order_date', 'id')
    readonly_fields = ('id',)

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderRowInline]
    list_display = ('car', 'user', 'status', 'order_rows','order_total_price', 'date')
    list_editable = ('status', 'user', 'date')
    list_filter = ('status', 'date', 'user')

admin.site.register(CarModel, CarModelAdmin)
admin.site.register(Car, CarAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(OrderRow, OrderRowAdmin)
