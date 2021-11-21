from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .models import ProductInBasket, Order, OrderItem
from .forms import CartAddProductForm


@require_POST
def cart_add(request, product_id):
    if not request.session.session_key:
        request.session.save()
    session = request.session.session_key
    product = get_object_or_404(Product, id=product_id)

    quantity = 1
    if 'quantity' in request.POST:
        quantity = request.POST['quantity']

    if request.user.is_authenticated:
        product_in_basket = ProductInBasket.objects.filter(product=product, author=request.user)
        if product_in_basket:
            product_in_basket.update(quantity=quantity, total_price=product.price * int(quantity))
        else:
            ProductInBasket.objects.create(session_key=session, product=product, author=request.user,
                                           price=product.price, total_price=product.price)
    else:
        product_in_basket = ProductInBasket.objects.filter(product=product, session_key=session)
        if product_in_basket:
            product_in_basket.update(quantity=quantity, total_price=product.price * int(quantity))
        else:
            ProductInBasket.objects.create(session_key=session, product=product,
                                           price=product.price, total_price=product.price)

    return redirect('cart:cart_detail')


def cart_remove(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        ProductInBasket.objects.filter(product=product, author=request.user).delete()
    else:
        session = request.session.session_key
        ProductInBasket.objects.filter(product=product, session_key=session).delete()

    return redirect('cart:cart_detail')


def clear_cart(request):
    if request.user.is_authenticated:
        ProductInBasket.objects.filter(author=request.user).delete()
    else:
        session = request.session.session_key
        ProductInBasket.objects.filter(session_key=session).delete()


def cart_detail(request):
    if request.user.is_authenticated:
        cart = ProductInBasket.objects.filter(author=request.user)
    else:
        session = request.session.session_key
        cart = ProductInBasket.objects.filter(session_key=session)

    total = get_total_price(cart)

    for item in cart:
        item.update_quantity_form = CartAddProductForm(initial={'quantity': item.quantity, 'update': True})

    return render(request, 'cart/detail.html', {'cart': cart, "total": total})


def cart_checkout(request):
    if request.user.is_authenticated:
        cart = ProductInBasket.objects.filter(author=request.user)
    else:
        session = request.session.session_key
        cart = ProductInBasket.objects.filter(session_key=session)

    total = get_total_price(cart)
    if request.method == "POST" and cart:
        first_name = request.POST.get('first-name', False)
        last_name = request.POST.get('last-name', False)
        email = request.POST.get('email', False)
        address = request.POST.get('address', False)
        city = request.POST.get('city', False)
        country = request.POST.get('country', False)
        zip_code = request.POST.get('zip-code', False)
        tel = request.POST.get('tel', False)

        shipping_first_name = request.POST.get('shiping-first-name', False)
        shipping_last_name = request.POST.get('shiping-last-name', False)
        shipping_email = request.POST.get('shiping-email', False)
        shipping_address = request.POST.get('shiping-address', False)
        shipping_city = request.POST.get('shiping-city', False)
        shipping_country = request.POST.get('shiping-country', False)
        shipping_zip_code = request.POST.get('shiping-zip-code', False)
        shipping_tel = request.POST.get('shiping-tel', False)

        if request.user.is_authenticated:
            order = Order.objects.create(author=request.user, first_name=first_name, last_name=last_name, email=email,
                                         address=address, city=city,
                                         country=country, zip_code=zip_code, tel=tel,
                                         shipping_first_name=shipping_first_name, shipping_last_name=shipping_last_name,
                                         shipping_email=shipping_email, shipping_address=shipping_address,
                                         shipping_city=shipping_city, shipping_country=shipping_country,
                                         shipping_zip_code=shipping_zip_code, shipping_tel=shipping_tel)
        else:
            session = request.session.session_key
            order = Order.objects.create(session_key=session, first_name=first_name, last_name=last_name, email=email,
                                         address=address, city=city,
                                         country=country, zip_code=zip_code, tel=tel,
                                         shipping_first_name=shipping_first_name, shipping_last_name=shipping_last_name,
                                         shipping_email=shipping_email, shipping_address=shipping_address,
                                         shipping_city=shipping_city, shipping_country=shipping_country,
                                         shipping_zip_code=shipping_zip_code, shipping_tel=shipping_tel)

        for item in cart:
            OrderItem.objects.create(order=order,
                                     product=item.product,
                                     price=item.price,
                                     quantity=item.quantity)

        clear_cart(request)
        return redirect("/")

    return render(request, 'cart/checkout.html', {'cart': cart, "total": total})


def get_total_price(cart):
    # we get the total cost
    return sum(Decimal(item.price) * item.quantity for item in cart)
