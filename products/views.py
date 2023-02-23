from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category, CouponCode


def all_products(request):
    """ A view to show all product details """
    products = Product.objects.all()
    query = None
    categories = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))

            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)

        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(
                    request, "You haven't entered anything to search for!")
                return redirect(reverse('products'))

            queries = Q(name__icontains=query) | Q(
                product_description__icontains=query)
            products = products.filter(queries)

    context = {
        "products": products,
        "search_term": query,
        "current_categories": categories,
    }

    return render(request, "products/products.html", context)


def product_detail(request, product_id):
    """ A view to show an individual product details """

    product = get_object_or_404(Product, pk=product_id)
    discount = CouponCode

    context = {
        "product": product,
        "discount": discount,
    }

    return render(request, "products/product_detail.html", context)


def sale_products(request):
    """ A view to show products that are on sale or have a deal on them """

    products = Product.objects.filter(
        coupon_codes__name='10%') | Product.objects.filter(deal__name='3for2')

    context = {
        "products": products,
    }

    return render(request, "products/sale_products.html", context)
