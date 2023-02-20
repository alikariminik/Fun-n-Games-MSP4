from django.db import models
from decimal import Decimal


class Category(models.Model):

    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Product (models.Model):
    uniq_id = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    category = models.ForeignKey(
        'Category', null=True, blank=True, on_delete=models.SET_NULL)
    sub_category1 = models.TextField(null=True, blank=True)
    sub_category2 = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    product_description = models.TextField()
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    variants = models.URLField(max_length=1024, null=True, blank=True)
    product_url = models.URLField(max_length=1024, null=True, blank=True)
    coupon_codes = models.ManyToManyField("products.CouponCode", blank=True)
    deal = models.ManyToManyField("products.Deal", blank=True)

    def __str__(self):
        return self.name

    def short_name(self):
        name_length = len(self.name)
        if name_length > 80:
            abbreviated_name = self.name[0:79]
            display_name = abbreviated_name + "..."
            return display_name
        return self.name

    def shorter_name(self):
        name_length = len(self.name)
        if name_length > 50:
            abbreviated_name = self.name[0:49]
            display_name = abbreviated_name + "..."
            return display_name
        return self.name

    def get_price(self):
        if self.coupon_codes.all():
            cc = self.coupon_codes.first()
            new_price = self.price - round(
                (Decimal(cc.percentage/100) * self.price), 2)
            return new_price
        return self.price


class CouponCode(models.Model):
    percentage = models.IntegerField()
    name = models.CharField(max_length=254)
    discount_amount = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name


class Deal(models.Model):
    name = models.CharField(max_length=254)
    eligible_quantity = models.IntegerField()
    saved_quantity = models.IntegerField()

    def __str__(self):
        return self.name
