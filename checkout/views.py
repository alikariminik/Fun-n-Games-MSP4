import stripe

from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse

from .forms import OrderForm
from . import urls

# Create your views here.

stripe.api_key = settings.STRIPE_SECRET_KEY


def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, '')
        return redirect(reverse('products'))

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51MeEiBFpgDYd3hANnwqFJXH8RjxFLT4jYNz5iumZz5PDtjDPcvggBHsNshxXnIY7u68DnFyaVhJewXhvt0htFGfe00iOXtij2N',
        'client_secret': 'sk_test_51MeEiBFpgDYd3hANLfclsr5NLyPrNHGHd5XeKdGZcKnnJHUIAjGA4HkiuIjt6zTo9iXbj2ZpLfjt70OKCMb0k3oN00tDojyrVa',
    }
    return render(request, template, context)


def create_payment(request):
    try:
        data = json.loads(request.data)
        intent = stripe.PaymentIntent.create(
            amount=20,
            currency="gbp"
        )

        return JsonResponse({
          'clientSecret': intent['client_secret']
        })
    except Exception as e:
        return jsonify(error=str(e)), 403
