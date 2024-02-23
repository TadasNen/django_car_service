from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Car, Order, Service, OrderRow
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages


def index(request):
    visit_count = request.session.get('visit_count', 0)
    visit_count += 1
    request.session['visit_count'] = visit_count

    total_cars = Car.objects.count()
    total_orders = Order.objects.count()
    total_services = Service.objects.count()

    context = {
        'total_cars': total_cars,
        'total_orders': total_orders,
        'total_services': total_services,
        'visit_count': visit_count,
    }
    return render(request, 'index.html', context)


def cars(request):
    car_list = Car.objects.all()
    cars_per_page = 6
    paginator = Paginator(car_list, cars_per_page)
    page = request.GET.get('page')
    try:
        cars = paginator.page(page)
    except PageNotAnInteger:
        cars = paginator.page(1)
    except EmptyPage:
        cars = paginator.page(paginator.num_pages)
    return render(request, 'cars.html', {'cars': cars})


def car_detail(request, pk):
    car = get_object_or_404(Car, pk=pk)
    return render(request, 'car_detail.html', {'car': car})


class OrderListView(generic.ListView):
    model = Order
    context_object_name = "orders"
    template_name = "orders.html"
    paginate_by = 5


class ServiceOrderByUserListView(LoginRequiredMixin, generic.ListView):
    model = Order
    template_name = 'user_orders.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('date')


def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_rows = order.order_row.all()
    return render(request, 'order_detail.html', {'order': order, 'order_rows': order_rows})


def search_results(request):
    query_text = request.GET.get("search_text", "")

    car_results = Car.objects.filter(
        Q(client__icontains=query_text) |
        Q(car_model__brand__icontains=query_text) |
        Q(car_model__model__icontains=query_text) |
        Q(license_plate__icontains=query_text) |
        Q(vin__icontains=query_text)
    )

    context = {
        "car_results": car_results,
        "query_text": query_text,
    }

    return render(request, "search_results.html", context=context)

@csrf_protect
def register_user(request):
    if request.method != "POST":
        return render(request, 'registration/registration.html')
    username = request.POST["username"]
    email = request.POST["email"]
    password = request.POST["password"]
    password2 = request.POST["password2"]

    if password != password2 :
        messages.error(request, "Passwords do not match!")

    if User.objects.filter(username=username).exists():
        messages.error(request, f"Username {username} is already taken!")

    if User.objects.filter(email=email).exists():
        messages.error(request, f"E-mail {email} is already being used!")

    if messages.get_messages(request):
        return redirect('register-url')

    User.objects.create_user(username=username, email=email, password=password)
    messages.success(request, f"User {username} created!")
    return redirect('login')