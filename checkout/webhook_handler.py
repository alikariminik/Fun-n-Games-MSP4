from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings


from .models import Order, OrderLineItem
from products.models import Product
from profiles.models import UserProfile


import json
import time


class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request

    def _send_confirmation_email(self, order):
        """Send User Confirmation Email"""
        cust_email = order.email
        subject = render_to_string(
            'checkout/confirmation_emails/confirmation_email_subject.txt',
            {'order': order})
        body = render_to_string(
            'checkout/confirmation_emails/confirmation_email_body.txt',
            {'order': order, 'contact_email': settings.DEFAULT_FROM_EMAIL})

        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [cust_email])

    def handle_event(self, event):
        """
        Handle a generic/unknown/unexpected webhook event
        """
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook from Stripe
        """
        intent = event.data.object
        pid = intent.id
        cart = intent.metadata.cart
        save_info = intent.metadata.save_info

        stripe_charge = stripe.Charge.retrieve(
            intent.latest_charge
        )

        billing_details = stripe_charge.billing_details
        shipping_details = intent.shipping
        total = round(stripe_charge.amount / 100, 2)

        for field, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[field] = None

        profile = None
        username = intent.metadata.username
        if username != 'Anonymous':
            profile = UserProfile.objects.get(user=username)
            if save_info:
                profile.default_phone_number = \
                    shipping_details.phone,
                profile.default_email = shipping_details.email,
                profile.default_street_address1 = \
                    shipping_details.address.line1,
                profile.default_street_address2 = \
                    shipping_details.address.line2,
                profile.default_town_or_city = shipping_details.address.city,
                profile.default_country = shipping_details.address.country,
                profile.default_postcode = \
                    shipping_details.address.postal_code,
                profile.default_county = shipping_details.address.state,
                profile.save()

        order_exisits = False
        attempt = 1
        while attempt <= 5:
            try:
                order = Order.Objects.get(
                    full_name__iexact=shipping_details.name,
                    phone_number__iexact=shipping_details.phone,
                    email__iexact=shipping_details.email,
                    street_address1__iexact=shipping_details.address.line1,
                    street_address2__iexact=shipping_details.address.line2,
                    town_or_city__iexact=shipping_details.address.city,
                    country__iexact=shipping_details.address.country,
                    postcode__iexact=shipping_details.address.postal_code,
                    county__iexact=shipping_details.address.state,
                    grand_total=grand_total,
                    original_cart=cart,
                    stripe_pid=pid,
                )
                order_exisits = True
                break
                return HttpResponse(
                    content=f'Webhood has been received: {event["type"]} | \
                    SUCCESS: Verified order already in database', status=200)

                return HttpResponse(
                    content=f'Webhook received: {event["type"]}',
                    status=200)
            except Order.DoesNotExist:
                attempt += 1
                time.sleep(1)
        if order_exisits:
            self._send_confirmation_email(order)
            return HttpResponse(
                content=f'Webhood has been received: {event["type"]} | \
                SUCCESS: Verified order already in database', status=200)
        else:
            order = None
            try:
                order = Order.objects.create(
                    full_name=shipping_details.name,
                    user_profile=profile,
                    phone_number=shipping_details.phone,
                    email=shipping_details.email,
                    street_address1=shipping_details.address.line1,
                    street_address2=shipping_details.address.line2,
                    town_or_city=shipping_details.address.city,
                    country=shipping_details.address.country,
                    postcode=shipping_details.address.postal_code,
                    county=shipping_details.address.state,
                    grand_total=grand_total,
                    original_cart=cart,
                    stripe_pid=pid,
                )
                for product_id, product_data in json.loads(cart).products():
                    product = Product.objects.get(id=product_id)
                    if isinstance(product_data, int):
                        order_line_item = OrderLineItem(
                            order=order,
                            product=product,
                            quantity=product_data,
                        )
                        order_line_item.save()
            except Exception as e:
                if order:
                    order.delete()
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | ERROR: {e}',
                    status=500)

        self._send_confirmation_email(order)
        return HttpResponse(
            content=f'Webhook has been received: \
            {event["type"]} | SUCCESS: Created order in webhook',
            status=200),

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)
