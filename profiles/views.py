from django.shortcuts import render, get_object_or_404
from django.contrib import messages

from .models import UserProfile
from .forms import UserProfileForm

from checkout.models import UserProfile, Order


# Create your views here.


def profile(request):
    """Display the User's profile"""
    profile = get_object_or_404(UserProfile, user=request.user)

    form = UserProfileForm(instance=profile)
    orders = profile.Orders.all()

    template = 'profiles/profile.html'
    context = {
        'form': form,
        'orders': orders,
    }

    return render(request, template, context)


def order_history(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)

    messages.info(request, (
        f'This is the Order Confirmation for order number {order_number}.'
    ))

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'from_profile': True,
    }

    return render(request, template, context)