from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, *args, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('type_user', User.TypeUserChoices.ADMIN)
        return self._create_user(*args, **kwargs)


class User(AbstractUser):
    class TypeUserChoices(models.TextChoices):
        ADMIN = ('admin', 'Administrator')
        CUSTOMER = ('customer', 'Customer')

    username = None
    email = models.EmailField(unique=True)
    type_user = models.CharField(max_length=50, default=TypeUserChoices.CUSTOMER, choices=TypeUserChoices.choices)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'.strip()

    @property
    def is_admin(self):
        return self.type_user == self.TypeUserChoices.ADMIN

    @property
    def is_customer(self):
        return self.type_user == self.TypeUserChoices.CUSTOMER
