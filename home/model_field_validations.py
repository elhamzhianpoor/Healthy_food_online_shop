from django.core.validators import ValidationError


def unit_price_validation(value):
    if value < 1 :
        raise ValidationError('must be at least 1$')
    return value
