from django.contrib.auth.models import UserManager as BaseUserManager
from uuid import uuid4


class UserManager(BaseUserManager):
    def _create_user(self, username=None, password=None, email='', first_name='', last_name='', **extra_fields):
        """
        Create and save a user with the given email, and password.
        """
        # if not email:
        #     raise ValueError('The email must be set')
        if not username:
            username = str(uuid4())
        if not password:
            password = self.make_random_password()
        if email is None:
            email = ''
        email = email.lower()
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        if first_name:
            first_name = first_name[:30]
        if last_name:
            last_name = last_name[:150]
        user = self.model(username=username, email=email, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username=username, password=password, email=email, **extra_fields)
