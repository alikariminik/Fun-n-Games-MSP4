from django.shortcuts import render, redirect, \
    reverse, get_object_or_404, HttpResponse
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.conf import settings

from .forms import OrderForm
from .models import OrderLineItem, Order

from products.models import Product

from profiles.forms import UserProfileForm
from profiles.models import UserProfile

from cart.contexts import cart_contents

import stripe
import json

# Create your views here.


def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        cart = request.session.get('cart', {})

        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'town_or_city': request.POST['town_or_city'],
            'county': request.POST['county'],
            'postcode': request.POST['postcode'],
            'country': request.POST['country'],
        }
        order_form = OrderForm(form_data)

        if order_form.is_valid():
            order = order_form.save(commit=False)
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid
            order.original_cart = json.dumps(cart)
            for product_id, product_data in cart.items():
                try:
                    product = Product.objects.get(id=product_id)
                    if isinstance(product_data, int):
                        order_line_item = OrderLineItem(
                            order=order,
                            product=product,
                            quantity=product_data,
                        )
                        order_line_item.save()
                except Product.DoesNotExist:
                    messages.error(request, (
                        "There is an issue relating to one of the \
                        products you tried to purchase. Please try again \
                        later and if the error persists, please contact us.")
                    )
                    order.delete()
                    return redirect(reverse('view_cart'))

            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse(
                'checkout_success', args=[order.order_number]))
        else:
            messages.error(request, 'There was an error with the information\
                you have provided. Please double check your information.')

    else:
        cart = request.session.get('cart', {})
        if not cart:
            messages.error(request, f'Your cart is empty!')
            return redirect(reverse(products))

        current_cart = cart_contents(request)
        total = current_cart['total']
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key

        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        if request.user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=request.user)
                order_form = OrderForm(initial={
                    'full_name': profile.user.get_full_name(),
                    'email': profile.user.email,
                    'phone_number': profile.default_phone_number,
                    'country': profile.default_country,
                    'postcode': profile.default_postcode,
                    'town_or_city': profile.default_town_or_city,
                    'street_address1': profile.default_street_address1,
                    'street_address2': profile.default_street_address2,
                    'county': profile.default_county,
                })
            except UserProfile.DoesNotExist:
                order_form = OrderForm()
        else:
            order_form = OrderForm()

    if not stripe_public_key:
        messages.warning(request, 'Missing: Stripe Public Key')

    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }
    return render(request, template, context)


def checkout_success(request, order_number):
    """Handle successfully completed checkouts"""

    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)

    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        order.user_profile = profile
        order.save()

        if save_info:
            profile_data = {
                'default_street_address1': order.street_address1,
                'default_street_address2': order.street_address2,
                'default_town_or_city': order.town_or_city,
                'default_county': order.county,
                'default_postcode': order.postcode,
                'default_country': order.country,
                'default_phone_number': order.phone_number,
            }
            user_profile_form = UserProfileForm(profile_data, instance=profile)
            if user_profile_form.is_valid():
                user_profile_form.save()

    messages.success(request, f'Your Order was Successful! \
        Your Order Number is {order_number}. \
        An email will sent to {order.email}  confirming this')

    if 'cart' in request.session:
        del request.session['cart']

    template = "checkout/checkout_success.html"
    context = {
        "order": order,
    }

    return render(request, template, context)


@require_POST
def cache_checkout_data(request):
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'username': request.user,
            'save_info': request.POST.get('save_info'),
            'cart': json.dumps(request.session.get('cart', {}))
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, "Something went wrong. Your payment could not \
        be processed this time. Please try again. ")
        return HttpResponse(content=e, status=400)
