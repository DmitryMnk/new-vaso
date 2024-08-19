from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, phone_number, name='', password=None):
        if not phone_number:
            raise ValueError("User must have a phone number")

        user = self.model(
            phone_number=phone_number,
            name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, name=''):
        user = self.create_user(
            phone_number=phone_number,
            password=password,
            name=name,
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user
