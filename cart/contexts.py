from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product


def cart_contents(request):

    cart_items = []
    sub_total = 0
    product_count = 0
    cart = request.session.get('cart', {})

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, pk=product_id)
        if product.get_price == product.price:
            sub_total += quantity * int(product.price)
            product_count += quantity
            cart_items.append({
                'product_id': product_id,
                'quantity': quantity,
                'product': product,
            })
        else:
            sale_price = product.get_price()
            sub_total += quantity * sale_price
            product_count += quantity
            cart_items.append({
                'product_id': product_id,
                'quantity': quantity,
                'products': product,
            })

    if sub_total < settings.FREE_DELIVERY:
        delivery = sub_total * Decimal(settings.STANDARD_DELIVERY / 100)
        free_delivery_remainder = settings.FREE_DELIVERY - sub_total
    else:
        delivery = 0
        free_delivery_remainder = 0

    total = delivery + sub_total

    context = {
        'cart_items': cart_items,
        'sub_total': sub_total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_remainder': free_delivery_remainder,
        'free_delivery': settings.FREE_DELIVERY,
        'total': total,
        'cart': cart,
    }

    return context
