from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product
import math


def get_product_total(product, quantity):
    if product.deal is not None:
        if product.deal.first() is not None:
            deal = product.deal.first()
            is_eligible = quantity / deal.eligible_quantity > 0
            if is_eligible:
                return (quantity
                        - math.floor(
                            quantity / deal.eligible_quantity)
                        * deal.saved_quantity) * product.get_price()
    return quantity * product.get_price()


def cart_contents(request):

    cart_items = []
    sub_total = 0
    product_count = 0
    quantity = 0
    cart = request.session.get('cart', {})

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, pk=product_id)

        if product.get_price() == product.price:
            sub_total += quantity * product.price
            product_count += quantity
            cart_items.append({
                'product_id': product_id,
                'quantity': quantity,
                'product': product,
                'product_sub_total': get_product_total(product, quantity),
                'product_non_discount': product.get_price() * quantity
            })
        else:
            sale_price = product.get_price()
            sub_total += quantity * sale_price
            product_count += quantity
            cart_items.append({
                'product_id': product_id,
                'quantity': quantity,
                'product': product,
                'sale_price': sale_price,
                'product_sub_total': quantity * sale_price,
                'product_non_discount': product.price * quantity

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
        'quantity': quantity,
    }

    return context
