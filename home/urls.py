from django.urls import path
from home import views

app_name = 'home'
urlpatterns = [
    path('',views.HomeView.as_view(),name='home'),
    path('products/',views.ProductView.as_view(),name='products'),
    path('products/<int:id>/<slug:slug>',views.ProductView.as_view(),name='category_products'),
    path('main_menu/<int:id>/<slug:slug>', views.MenuView.as_view(), name='menu_products'),
    path('menu_item/<int:id>/<slug:slug>',views.MenuItemView.as_view(), name='menu_item_products'),
    path('details/<int:id>/<slug:slug>/',views.ProductDetailsView.as_view(),name='details'),
    path('details/<int:id>/<slug:slug>/<int:com_id>', views.ProductDetailsView.as_view(), name='reply'),
    path('comment_like/',views.CommentLikeView.as_view(),name='comment_like'),
    path('comment_dislike/', views.CommentDislikeView.as_view(), name='comment_dislike'),
    path('product_like/',views.ProductLikeView.as_view(), name='product_like'),

]