from django.urls import path
from cart import views
from django.views.decorators.csrf import csrf_exempt

app_name = 'cart'
urlpatterns = [
    path('cart/', views.CartView.as_view(), name='cart'),
    path('add/cart/<int:p_id>', views.AddToCartView.as_view(), name='add_to_cart'),
    path('add/variant_cart/<int:v_id>', views.AddToVariantCartView.as_view(), name='add_to_variant_cart'),
    path('cart/remove/<int:p_id>', views.ProductRemoveView.as_view(), name='remove_from_cart'),
    path('cart/remove_var/<int:v_id>', views.VariantRemoveView.as_view(), name='var_remove_from_cart'),
    path('cart/add_one/<int:p_id>', views.ProductAddOneView.as_view(), name='product_add_one'),
    path('cart/remove_one/<int:p_id>', views.ProductRemoveOneView.as_view(), name='product_remove_one'),
    path('cart/variant_add_one/<int:v_id>', views.VariantAddOneView.as_view(), name='variant_add_one'),
    path('cart/variant_remove_one/<int:v_id>', views.VariantRemoveOneView.as_view(), name='variant_remove_one'),
    path('order/checkout/<int:order_id>', views.OrderCheckoutView.as_view(), name='order_checkout'),
    path('order/create/', views.OrderCreateView.as_view(), name='order_create'),
    path('order/start-pay/<int:order_id>',views.StartPayView.as_view(), name='start_pay'),
    path('order/verify-payment/',csrf_exempt(views.VerifyPaymentView.as_view()), name='verify_payment'),


]
