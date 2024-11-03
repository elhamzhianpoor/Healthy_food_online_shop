from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from accounts.forms import UserCreationForm,UserChangeForm
from django.contrib.auth.models import Group
from accounts.models import User,Otp


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('phone_number','email','first_name','last_name','is_active')
    list_filter = ('is_active',)
    fieldsets = (
        (None,
         {'fields':('email','first_name','last_name','phone_number','address','password')}
         ),
        (
            'permissions',
            {'fields':('is_superuser','is_active','is_admin','groups','user_permissions','last_login')}
        )
    )
    add_fieldsets =(
        (None,
         {'fields':('phone_number','email','first_name','last_name','password1','password2')}
         ),
    )
    search_fields = ('phone_number','email')
    ordering = ('first_name',)
    filter_horizontal = ('groups','user_permissions')

    def get_form(self, request,obj=None,**kwargs):
        form = super().get_form(request,obj,**kwargs)
        if not request.user.is_superuser:
            form.base_fields['is_superuser'].disabled = True
        return form

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(id=request.user.id)

        return qs


class OtpAdmin(admin.ModelAdmin):
    list_display = ('phone_number','code','created')


admin.site.register(Otp, OtpAdmin)
# admin.site.unregister(Group)
admin.site.register(User,UserAdmin)
