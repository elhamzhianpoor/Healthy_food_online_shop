from django.urls import path
from accounts import views

app_name = 'accounts'
urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('verify-register/', views.VerifyRegisterView.as_view(), name='verify_register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('reset/', views.UserPasswordResetView.as_view(), name='password_reset'),
    path('reset/done/', views.UserPasswordResetDoneView.as_view(), name='reset_done'),
    path('reset/confirm/<uidb64>/<token>', views.UserPasswordResetConfirmView.as_view(), name='reset_confirm'),
    path('reset/complete/', views.UserPasswordResetCompleteView.as_view(), name='reset_complete'),
    path('profile/',views.ProfileView.as_view(), name='profile'),
    path('profile/update/',views.ProfileEditView.as_view(), name='profile_update'),
    path('favourite/',views.FavouriteProductView.as_view(), name='favourite_user'),
    path('change-password/',views.UserChangePasswordView.as_view(), name='change_password'),
    path('order_history/',views.OrderHistoryView.as_view(), name='order_history'),
    path('view/',views.RecentViewsView.as_view(), name='recent_view'),

]
