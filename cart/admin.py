from django.contrib import admin
from cart.cart import Cart
from cart.models import *


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    # fields = ('size','unit_price','stock','discount','available',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'paid', 'created', 'modified')
    inlines = [OrderItemInline,]


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code','active','discount','from_date','to_date')