from decimal import Decimal
from django.conf import settings


def cart_contents(request):

    cart_items = []
    sub_total = 0
    product_count = 0

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
    }

    return context
