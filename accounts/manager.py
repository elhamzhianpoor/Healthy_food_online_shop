from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, phone_number, email, password, first_name=None, last_name=None, address=None):
        if not phone_number:
            raise ValueError('Phone number must be set')
        if not email:
            raise ValueError('Email must be set')
        user = self.model(
            phone_number = phone_number,email = email,first_name=first_name,last_name=last_name,address=address
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,phone_number, email, password, first_name=None, last_name=None, address=None):
        user = self.create_user(phone_number, email, password,first_name,last_name,address)
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
