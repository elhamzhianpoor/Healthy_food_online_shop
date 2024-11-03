from cart.cart import Cart,VariantCart


def cart_context_processor(request):
    return {
        'cart_len': Cart(request).__len__() + VariantCart(request).__len__()
    }


