from django.shortcuts import render, redirect, reverse, HttpResponse
from django.contrib import messages
from products.models import Product


# Create your views here.


def view_cart(request):
    """ A view that renders the cart's contents page page """

    return render(request, 'cart/cart.html')


#  Code Institute Lessons - Boutique Ado
def add_to_cart(request, product_id):
    """ Add a quantity of the specified product to the cart """
    product = Product.objects.get(pk=product_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    cart = request.session.get('cart', {})

    if product_id in list(cart.keys()):
        cart[product_id] += quantity
        messages.success(
            request, f'{quantity}x {product.shorter_name()} has been added to \
            your cart.')
    else:
        cart[product_id] = quantity
        messages.success(
            request, f'{quantity}x {product.shorter_name()} has been added to \
            your cart.')

    request.session['cart'] = cart

    return redirect(redirect_url)


#  Code Institute Lessons - Boutique Ado
def adjust_cart(request, product_id):
    """Adjust the quantity of the specified product to the specified amount"""

    quantity = int(request.POST.get('quantity'))
    cart = request.session.get('cart', {})

    if quantity > 0:
        cart[product_id] = quantity
    else:
        cart.pop(product_id)

    request.session['cart'] = cart
    return redirect(reverse('view_cart'))


#  Code Institute Lessons - Boutique Ado
def remove_from_cart(request, product_id):
    """Remove the product from the cart"""

    try:
        cart = request.session.get('cart', {})
        cart.pop(product_id)
        request.session['cart'] = cart
        return HttpResponse(status=200)
    except Exception as e:
        return HttpResponse(status=500)
