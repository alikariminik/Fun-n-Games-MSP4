from django.shortcuts import render

# Create your views here.


def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, '')
        return redirect(reverse('products'))

    order_form = OrderForm
