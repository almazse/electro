from decimal import Decimal

from cart.models import ProductInBasket


def cart(request):
    if request.user.is_authenticated:
        widget_cart = ProductInBasket.objects.filter(author=request.user)
    else:
        session = request.session.session_key
        widget_cart = ProductInBasket.objects.filter(session_key=session)
    widget_cart_count = widget_cart.__len__()
    widget_cart_total = sum(Decimal(item.price) * item.quantity for item in widget_cart)

    return locals()