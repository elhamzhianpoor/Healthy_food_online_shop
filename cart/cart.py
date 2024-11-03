from home.models import Product, Variant
from decimal import Decimal
CART_SESSION_ID = 'cart'
VARIANT_CART_KEY = 'var_cart'


class Cart:
    def __init__(self, request):
        self.session = request.session
        if not self.session.get(CART_SESSION_ID):
            self.session[CART_SESSION_ID] = {}

        self.cart = self.session[CART_SESSION_ID]

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for p in products:
            cart[str(p.id)]['product'] = p.name
            cart[str(p.id)]['image'] = str(p.image)
            cart[str(p.id)]['id'] = p.id
            cart[str(p.id)]['discount'] = p.discount
            cart[str(p.id)]['price'] = str(p.final_price)
            cart[str(p.id)]['unit_price'] = str(p.unit_price)
            cart[str(p.id)]['get_absolute_url'] = p.get_absolute_url()
        for item in cart.values():
            item['total_price'] = (item['quantity']) * float(item['price'])
            yield item

    def __len__(self):
        # return sum(item['quantity']for item in self.cart.values())
        return sum(1 for item in self.cart.values())

    def save(self):
        self.session.modified = True

    def add(self, product, quantity):
        p_id = str(product.id)
        if p_id not in self.cart:
            self.cart[p_id] = {'quantity': 0, 'price': str(product.final_price)}
        if self.cart[p_id]['quantity'] + quantity > product.stock:
            return False
        self.cart[p_id]['quantity'] += quantity
        self.save()

    def remove(self, product, quantity=None):
        product_id = str(product.id)
        if product_id in self.cart:
            if not quantity:
                del self.cart[product_id]
                self.save()
            else:
                if self.cart[product_id]['quantity'] > 1:
                    self.cart[product_id]['quantity'] -= quantity
                    self.save()
                else:
                    self.remove(product)

    @property
    def total(self):
        return sum((item['quantity']) * float(item['price']) for item in self.cart.values())
        
    def clear(self):
        del self.session[CART_SESSION_ID]
        self.save()


class VariantCart:
    def __init__(self, request):
        self.session = request.session
        variant_cart = self.session.get(VARIANT_CART_KEY)
        if not variant_cart:
            self.session[VARIANT_CART_KEY] = {}

        self.variant_cart = self.session[VARIANT_CART_KEY]

    def __len__(self):
        # return sum(item['quantity']for item in self.variant_cart.values())
        return sum(1 for item in self.variant_cart.values())

    def __iter__(self):
        var_ids = self.variant_cart.keys()
        variants = Variant.objects.filter(id__in=var_ids)
        variant_cart = self.variant_cart.copy()
        for v in variants:
            variant_cart[str(v.id)]['variant'] = v.product.name
            variant_cart[str(v.id)]['image'] = str(v.product.image)
            variant_cart[str(v.id)]['id'] = v.id
            variant_cart[str(v.id)]['discount'] = v.discount
            variant_cart[str(v.id)]['size'] = v.size.name
            variant_cart[str(v.id)]['price'] = str(v.final_price)
            variant_cart[str(v.id)]['unit_price'] = str(v.unit_price)
            variant_cart[str(v.id)]['get_absolute_url'] = v.product.get_absolute_url()
        for item in variant_cart.values():
            item['total_price'] =(item['quantity']) * float(item['price'])
            yield item

    def save(self):
        self.session.modified = True

    def add(self, variant, quantity):
        var_id = str(variant.id)
        if var_id not in self.variant_cart:
            self.variant_cart[var_id] = {'quantity': 0, 'price': str(variant.final_price)}
        if self.variant_cart[var_id]['quantity'] + quantity > variant.stock:
            return False
        self.variant_cart[var_id]['quantity'] += quantity
        self.save()

    def remove(self, variant, quantity=None):
        v_id = str(variant.id)
        if v_id in self.variant_cart:
            if not quantity:
                del self.variant_cart[v_id]
                self.save()
            else:
                if self.variant_cart[v_id]['quantity'] > 1:
                    self.variant_cart[v_id]['quantity'] -= quantity
                    self.save()
                else:
                    self.remove(variant)

    @property
    def total(self):
        return sum((item['quantity']) * float(item['price'])for item in self.variant_cart.values())

    def clear(self):
        del self.session[VARIANT_CART_KEY]
        self.save()

