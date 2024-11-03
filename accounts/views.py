from datetime import timedelta, datetime
from pyexpat.errors import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from accounts.forms import UserRegisterForm, OtpForm, LoginForm, UserUpdateForm
from accounts.models import User, Otp
from utils.sms import send_otp
from random import randint
from django.contrib import messages
from django.contrib.auth import views as auth_views, authenticate,login,logout
from cart.cart import CART_SESSION_ID, VARIANT_CART_KEY
from django.contrib.auth import update_session_auth_hash


class UserRegisterView(View):
    form_class = UserRegisterForm
    template_name = 'accounts/register.html'

    def get(self, request):
        form = self.form_class()
        ctx = {
            'form': form
        }
        return render(request, self.template_name, ctx)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            rand_code = randint(100000, 999999)
            if otp := Otp.objects.filter(phone_number=cd.get('phone_number')):
                otp.delete()
            Otp.objects.create(phone_number=cd.get('phone_number'), code=rand_code)
            send_otp(cd.get('phone_number'), rand_code)
            request.session['user_info'] = {
                'phone_number': cd.get('phone_number'),
                'email': cd.get('email'),
                'first_name': cd.get('first_name'),
                'last_name': cd.get('last_name'),
                'password': cd.get('password1'),
            }
            messages.success(request, f'{rand_code}', extra_tags='success')
            return redirect('accounts:verify_register')

        ctx = {
            'form': form
        }
        messages.error(request, 'error message',extra_tags='error')
        return render(request, self.template_name, ctx)


class VerifyRegisterView(View):
    form_class = OtpForm
    template_name = 'accounts/verify-register.html'

    def get(self, request):
        ctx = {
            'form': self.form_class(),
        }
        return render(request, self.template_name, ctx)

    def post(self, request):
        user_info = request.session.get('user_info')
        otp_instance = Otp.objects.filter(phone_number=user_info.get('phone_number')).first()
        form = self.form_class(request.POST)
        if form.is_valid():
            user_code = form.cleaned_data['code']

            if user_code != otp_instance.code:
                messages.add_message(request, 200, 'otps not match!', 'warning')
                return redirect('accounts:verify_register')

            otp_exp = otp_instance.created + timedelta(minutes=2)
            now = datetime.now().astimezone(tz=otp_exp.tzinfo)
            if now > otp_exp:
                messages.add_message(request, 200, 'expired', 'danger')
                del request.session['user_info']
                otp_instance.delete()
                return redirect('accounts:register')

            User.objects.create_user(
                phone_number=user_info.get('phone_number'),
                email=user_info.get('email'),
                first_name=user_info.get('first_name'),
                last_name=user_info.get('last_name'),
                password=user_info.get('password'),
            )

            messages.add_message(request, 200, 'registered successfully', 'success')
            return redirect('accounts:login')

        ctx = {
            'form': form,
        }

        return render(request, self.template_name, ctx)


class LoginView(View):
    template_name = 'accounts/login.html'
    form_class = LoginForm

    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get('next')
        return super().setup(request, *args, **kwargs)

    def get(self,request):
        ctx = {
            'form': self.form_class()
        }
        return render(request, self.template_name, ctx)

    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,username=cd.get('phone_number'),password=cd.get('password'))
            if user:
                login(request,user)
                if self.next:
                    return redirect(self.next)
                else:
                    return redirect('home:home')

        ctx = {
            'form': self.form_class
        }
        messages.add_message(request,200,'user or password is wrong','danger')
        return render(request, self.template_name, ctx)


class LogoutView(View):
    def get(self,request):
        cart = request.session.get(CART_SESSION_ID)
        var_cart = request.session.get(VARIANT_CART_KEY)
        logout(request)
        if cart:
            request.session[CART_SESSION_ID] = cart
        if var_cart:
            request.session[VARIANT_CART_KEY] = var_cart
        return redirect('home:home')


class UserPasswordResetView(auth_views.PasswordResetView):
    template_name = 'accounts/password-reset-form.html'
    success_url = reverse_lazy('accounts:reset_done')
    email_template_name = 'accounts/password-reset-email.html'


class UserPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'accounts/password-reset-done.html'


class UserPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'accounts/password-reset-confirm.html'
    success_url = reverse_lazy('accounts:reset_complete')


class UserPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'accounts/password-reset-complete.html'


class ProfileView(View):
    def get(self,request):
        return render(request, 'accounts/profile.html')


class ProfileEditView(View,LoginRequiredMixin):
    form_class = UserUpdateForm
    template_name = 'accounts/edit_profile.html'

    def get(self,request):
        ctx = {
            'form': self.form_class(instance=request.user)
        }
        return render(request, self.template_name, ctx)

    def post(self,request):
        form = self.form_class(request.POST,instance=request.user)
        if form.is_valid():
            form.save()
            messages.add_message(request, 200, 'Your profile has been updated!', 'success')
            return redirect('accounts:profile')
        return render(request,self.template_name,{'form':form})


class UserChangePasswordView(View,LoginRequiredMixin):
    form_class = PasswordChangeForm
    template_name = 'accounts/change_password.html'

    def get(self,request):
        ctx = {
            'form': self.form_class(request.user)
        }
        return render(request, self.template_name, ctx)

    def post(self,request):
        form = self.form_class(request.user,request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request,form.user)
            messages.add_message(request, 200, 'Your password has been changed!', 'success')
            return redirect('accounts:profile')
        ctx = {
            'form': form
        }
        return render(request, self.template_name, ctx)