from decimal import Decimal

from django.db import models

from accounts.models import User
from home.models import Product, Variant
from utils.base_model import BaseModel


class Order(BaseModel):
    user = models.ForeignKey('accounts.User', models.SET_NULL, null=True, related_name='orders')
    phone_number = models.CharField(max_length=11, null=True)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    invoice_id = models.CharField(max_length=255, null=True)
    trans_id = models.TextField(null=True)
    card_number = models.CharField(max_length=16,null=True)
    bank = models.CharField(max_length=100, null=True)
    tracking_number = models.CharField(max_length=255, null=True)
    status = models.CharField(max_length=100, null=True)
    address = models.TextField(null=True)
    paid = models.BooleanField(default=False)
    error = models.CharField(max_length=100, null=True)
    discount = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.user.phone_number

    def get_total_price(self):
        return sum(
            item.get_price for item in self.order_items.all()
        )

    @property
    def shipping(self):
        shipping_cost = Decimal(self.get_total_price() / 10000)
        return shipping_cost

    @property
    def final_cost(self):
        final_cost = self.get_total_price() + self.shipping

        if self.discount:
            return (100 - self.discount) * final_cost // 100
        else:
            return final_cost


class OrderItem(BaseModel):
    order = models.ForeignKey(Order, models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, models.SET_NULL, null=True, blank=True, related_name='p_items')
    variant = models.ForeignKey(Variant, models.SET_NULL, null=True, blank=True, related_name='v_items')
    quantity = models.PositiveIntegerField(default=0)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        if self.product:
            return f'{self.order.user.phone_number} - {self.product.name}'
        if self.variant:
            return f'{self.order.user.phone_number} - {self.variant.product.name}'

    # @property
    # def get_final_price(self):
    #     final_price = self.unit_price
    #     if self.product.discount:
    #         final_price = (100 - self.product.discount) * final_price // 100
    #         return final_price
    #     if self.variant.discount:
    #         final_price = (100 - self.variant.discount) * final_price // 100
    #         return final_price

    @property
    def get_price(self):
        # if self.product.discount:
        #     return self.quantity * self.get_final_price
        # if self.variant.discount:
        #     return self.quantity * self.get_final_price

        return self.quantity * self.unit_price


class Coupon(BaseModel):
    code = models.CharField(max_length=100, unique=True)
    discount = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    # user = models.ManyToManyField(User, related_name='coupons')
    from_date = models.DateTimeField()
    to_date = models.DateTimeField()

    def __str__(self):
        return self.code


class Compare(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return self.product.name


