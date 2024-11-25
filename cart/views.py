from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from cart.models import Order, OrderItem, Coupon
from home.models import Product, DietCategory, Variant
from cart.cart import Cart, VariantCart
from cart.forms import CartForm, UserInfoForm, CouponForm
from django.contrib import messages
from django.shortcuts import get_object_or_404
import uuid
from utils import pg


class CartView(View):
    def get(self, request):
        cart = Cart(request)
        var_cart = VariantCart(request)
        ctx = {
            'cart': cart,
            'var_cart': var_cart,
            'diet_list': DietCategory.objects.all(),
        }
        return render(request, 'cart/cart.html', ctx)


class AddToCartView(View):
    def post(self, request, p_id):
        product = Product.objects.filter(id=p_id).first()
        form = CartForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            cart = Cart(request)
            cart.add(product, quantity)

            messages.add_message(request, 200, 'your product successful add ', 'success')
            return redirect('home:details', product.id, product.slug)
        messages.add_message(request, 200, 'your product failed add ', 'error')
        return redirect('home:products')


class ProductRemoveView(View):
    def get(self, request, p_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=p_id)
        if product:
            cart.remove(product)
            messages.add_message(request, 200, 'removed successfully ', 'success')

        return redirect('cart:cart')


class VariantRemoveView(View):
    def get(self, request, v_id):
        var_cart = VariantCart(request)
        variant = get_object_or_404(Variant, id=v_id)
        if variant:
            var_cart.remove(variant)
            messages.add_message(request, 200, 'removed successfully ', 'success')

        return redirect('cart:cart')


class OrderCheckoutView(LoginRequiredMixin, View):
    template_name = 'cart/order-checkout.html'

    def get(self, request, order_id):
        ctx = {
            'order': get_object_or_404(Order, id=order_id),
            'coupon_form': CouponForm()
        }
        return render(request, self.template_name, ctx)

    def post(self, request, order_id):
        form = CouponForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            order = get_object_or_404(Order, id=order_id)
            now = datetime.now()
            if coupon := Coupon.objects.filter(code__exact=code, active=True, from_date__lte=now,
                                               to_date__gte=now).first():
                order.discount = coupon.discount
                order.save()
                messages.add_message(request, 200, 'Your coupon has been applied.', 'success')
                return redirect('cart:order_checkout', order.id)
            messages.add_message(request, 200, 'Your coupon has been expired.', 'error')
            return redirect('cart:order-checkout', order.id)
        ctx = {
            'order': get_object_or_404(Order, id=order_id),
            'coupon_form': form
        }
        messages.add_message(request, 200, 'Your coupon do not work .', 'error')
        return render(request, self.template_name, ctx)


class OrderCreateView(LoginRequiredMixin, View):
    form_class = UserInfoForm
    template_name = 'cart/order-create.html'

    def get(self, request):
        ctx = {
            'form': self.form_class(instance=request.user),
        }
        return render(request, self.template_name, ctx)

    def post(self, request):
        form = self.form_class(request.POST)
        cart = Cart(request)
        var_cart = VariantCart(request)
        if form.is_valid():
            cd = form.cleaned_data
            order = Order.objects.create(
                user=request.user,
                phone_number=cd.get('phone_number'),
                first_name=cd.get('first_name'),
                last_name=cd.get('last_name'),
                address=cd.get('address'),
            )
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product_id=item['id'],
                    quantity=item['quantity'],
                    unit_price=item['price'],
                )

            for item in var_cart:
                obj = OrderItem.objects.create(
                    order=order,
                    variant_id=item['id'],
                    quantity=item['quantity'],
                    unit_price=item['price'],
                )
                obj.product = obj.variant.product
                obj.save()
            messages.add_message(request, 200, 'Your cart deleted.', 'success')
            cart.clear()
            var_cart.clear()
            return redirect('cart:order_checkout', order.id)
        return render(request, self.template_name, {'form': form})


class ProductAddOneView(View):
    def get(self, request, p_id):
        product = get_object_or_404(Product, id=p_id)
        if product:
            cart = Cart(request)
            cart.add(product, 1)
            return redirect('cart:cart')
        return redirect('cart:cart')


class ProductRemoveOneView(View):
    def get(self, request, p_id):
        product = get_object_or_404(Product, id=p_id)
        if product:
            cart = Cart(request)
            cart.remove(product, 1)
            return redirect('cart:cart')
        return redirect('cart:cart')


class AddToVariantCartView(View):
    def post(self, request, v_id):
        variant = get_object_or_404(Variant, id=v_id)
        form = CartForm(request.POST)
        if variant:
            if form.is_valid():
                quantity = form.cleaned_data['quantity']
                cart = VariantCart(request)
                cart.add(variant, quantity=quantity)

                messages.add_message(request, 200, 'your product successful add ', 'success')
                return redirect('home:details', variant.product.id, variant.product.slug)
            messages.add_message(request, 200, 'your product failed add ', 'error')
            return redirect('home:products')
        return redirect('home:details', variant.product.id, variant.product.slug)


class VariantAddOneView(View):
    def get(self, request, v_id):
        variant = get_object_or_404(Product, id=v_id)
        if variant:
            cart = VariantCart(request)
            cart.add(variant, 1)
            return redirect('cart:cart')
        return redirect('cart:cart')


class VariantRemoveOneView(View):
    def get(self, request, v_id):
        variant = get_object_or_404(Product, id=v_id)
        if variant:
            cart = VariantCart(request)
            cart.remove(variant, 1)
            return redirect('cart:cart')
        return redirect('cart:cart')


class StartPayView(LoginRequiredMixin, View):
    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        invoice_id = str(uuid.uuid4())
        order.invoice_id = invoice_id
        order.save()
        if order:
            data = {
                'amount': order.final_cost,
                'invoice_id': invoice_id
            }
            response = pg.pg_create(data)
            res = response.json()
            if response.status_code == 200:
                if res.get('status') == 'success':
                    order.trans_id = res.get('transid')
                    order.save()
                    messages.add_message(request, 200, 'Your payment was successful  ', 'success')
                    return redirect(f'https://panel.aqayepardakht.ir/startpay/sandbox/{order.trans_id}')
                messages.add_message(request, 200, 'Your payment was not successful ', 'success')
                return redirect('home:home')
            print(res)
            messages.add_message(request, 200, 'Your payment has error ', 'success')
            return redirect('home:home')


class VerifyPaymentView(View):
    def post(self, request):
        data = request.POST
        if order := get_object_or_404(Order, invoice_id=data.get('invoice_id')):
            order.trans_id = data.get('transid')
            order.card_number = data.get('cardnumber')
            order.tracking_number = data.get('tracking_number')
            order.bank = data.get('bank')
            order.status = data.get('status')
            order.save()
            data = {
                'amount': order.final_cost,
                'transid': order.trans_id,
            }
            response = pg.pg_verify(data)
            res = response.json()
            if response.status_code == 200 and res.get('status') == 'success' and res.get('code') == '1':
                order.paid = True
                order.save()
                products = order.order_items.all()
                for p in products:
                    if not p.variant:
                        product = Product.objects.filter(id=p.product_id).first()
                        product.stock -= p.quantity
                        product.sell += p.quantity
                        product.save()
                    else:
                        variant = Variant.objects.filter(id=p.variant_id).first()
                        variant.stock -= p.quantity
                        variant.sell += p.quantity
                        variant.save()

                return render(request, 'cart/verify-payment.html', {'order': order})

            error = pg.pg_get_error(res.get('code'))
            order.error = error
            order.save()
            return render(request, 'cart/verify-payment.html', {'order': order})

        return render(request, '404.html')
