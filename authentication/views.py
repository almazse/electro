from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect
from .forms import UserLoginForm, AdminAddProductForm, AdminPaidStatusForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib import messages
from .models import Profile
from cart.models import Order, OrderItem
from shop.models import Product
from django.utils import timezone


def user_login(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            client_data = form.cleaned_data
            user = authenticate(username=client_data['login'], password=client_data['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, "Authenticated successful!")
                    return redirect("/")
                else:
                    return HttpResponse('User blocked!')
            else:
                return HttpResponse('Authenticated blocked!')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect("authentication:login")


def sign_in(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        city = request.POST['city']
        phone = request.POST['phone']

        user = User.objects.create_user(username=username, email=email, password=password)

        user.first_name = first_name
        user.last_name = last_name

        Profile.objects.create(user=user, city=city, phone=phone)

        group = Group.objects.get(name='customers')
        group.user_set.add(user)

        user.save()

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, "Authenticated successful!")
                return redirect("/")
            else:
                return HttpResponse('User blocked!')
        else:
            return HttpResponse('Authenticated blocked!')

    return render(request, 'signin.html')


def user_page(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(author=request.user)
        items = []
        for order in orders:
            items_order = OrderItem.objects.filter(order=order)
            for item in items_order:
                items.append({"order_id": order.id, "product": item.product, "price": item.price, "quantity": item.quantity})

        return render(request, 'user.html', {'orders': orders, "items": items})
    else:
        return redirect("/")


def admin_page(request):
    if request.user.is_authenticated and request.user.is_staff:

        if request.POST:
            order = Order.objects.filter(id=request.POST['order-id'])
            if 'paid' in request.POST:
                order.update(paid=True)
            else:
                order.update(paid=False)

        orders = Order.objects.filter()
        items_top_selling = {}
        items = []
        for order in orders:
            items_order = OrderItem.objects.filter(order=order)
            for item in items_order:
                items.append({"order_id": order.id, "product": item.product, "price": item.price,
                              "quantity": item.quantity})

                if item.product.name in items_top_selling:
                    items_top_selling[item.product.name] += item.quantity
                else:
                    items_top_selling[item.product.name] = item.quantity

            order.update_paid = AdminPaidStatusForm(initial={'paid': order.paid, 'update': True})

        return render(request, 'admin.html', {'orders': orders, "items": items,
                                              "items_top_selling": items_top_selling})
    else:
        return redirect("/")


def admin_page_top(request):
    if request.user.is_authenticated and request.user.is_staff:
        orders = Order.objects.filter()
        items_top_selling = {}
        for order in orders:
            items_order = OrderItem.objects.filter(order=order)
            for item in items_order:
                if item.product.name in items_top_selling:
                    items_top_selling[item.product.name] += item.quantity
                else:
                    items_top_selling[item.product.name] = item.quantity
        items_top_selling = sorted(items_top_selling.items(), key=lambda x: x[1], reverse=True)
        return render(request, 'admin_top.html', {"items_top_selling": items_top_selling})
    else:
        return redirect("/")


def admin_page_products(request):
    if request.user.is_authenticated and request.user.is_staff:
        products = Product.objects.all()

        return render(request, 'admin_products.html', {"products": products})
    else:
        return redirect("/")


def admin_page_add_product(request):
    if request.user.is_authenticated and request.user.is_staff:
        if request.method == "POST":
            form = AdminAddProductForm(request.POST, request.FILES)
            if form.is_valid():
                products = form.save(commit=False)
                products.updated = timezone.now()
                products.save()
                return redirect("/authentication/admin/products/")
        else:
            form = AdminAddProductForm()

        return render(request, 'admin_add_product.html', {"form": form})
    else:
        return redirect("/")
