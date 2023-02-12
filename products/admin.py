from django.contrib import admin
from .models import Product, Category


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
        "variants",
        "product_url",
    )


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "friendly_name",
    )


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
