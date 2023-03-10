from django.contrib import admin
from .models import Product, Category, CouponCode, Deal


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "uniq_id",
        "name",
        "category",
        "sub_category1",
        "sub_category2",
        "price",
        "product_description",
        "image_url",
        "product_url",
    )


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "friendly_name",
    )


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(CouponCode)
admin.site.register(Deal)
