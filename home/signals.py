from django.db.models.signals import post_save
from django.dispatch import receiver
from home.models import Product, PriceChange, Variant


@receiver(post_save, sender=Product)
def price_change_handler(**kwargs):
    product = kwargs['instance']
    PriceChange.objects.get_or_create(product=product, unit_price=product.unit_price)


@receiver(post_save, sender=Variant)
def var_price_change_handler(**kwargs):
    variant = kwargs['instance']
    PriceChange.objects.get_or_create(variant=variant, unit_price=variant.unit_price)