import django_filters
from django import forms
from .models import *


class ProductFilter(django_filters.FilterSet):
    choice_price = {
        ('expensive', 'expensive'),
        ('inexpensive', 'inexpensive'),
    }
    choice_create = {
        ('Newest', 'newest'),
        ('oldest', 'oldest'),

    }
    choice_discount = {
        ('most discount', 'most discount'),
        ('low discount', 'low discount'),
    }
    choice_sell = {
        ('most sell', 'most sell'),
        ('low sell', 'low sell'),

    }
    price_1 = django_filters.NumberFilter(field_name='unit_price', lookup_expr='gte')
    price_2 = django_filters.NumberFilter(field_name='unit_price', lookup_expr='lte')
    size = django_filters.ModelMultipleChoiceFilter(queryset=Size.objects.all(),widget=forms.CheckboxSelectMultiple)
    price = django_filters.ChoiceFilter(choices=choice_price,method='price_filter')
    created = django_filters.ChoiceFilter(choices=choice_create,method='create_filter')
    discount = django_filters.ChoiceFilter(choices=choice_discount,method='discount_filter')
    sell = django_filters.ChoiceFilter(choices=choice_sell,method='sell_filter')
    def price_filter(self, queryset, name, value):
        data = 'unit_price' if value == 'inexpensive' else '-unit_price'
        return queryset.order_by(data)

    def create_filter(self, queryset, name, value):
        data = 'created' if value == 'oldest' else '-created'
        return queryset.order_by(data)

    def discount_filter(self, queryset, name, value):
        data = 'discount' if value == 'low discount' else '-discount'
        return queryset.order_by(data)

    def sell_filter(self, queryset, name, value):
        data = 'sell' if value == 'low sell' else '-sell'
        return queryset.order_by(data)