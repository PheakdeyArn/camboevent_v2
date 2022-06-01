from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


class MyUserManager(BaseUserManager):

    def _create_user(self, email, first_name, last_name, phone_number, password, is_staff, is_superuser, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            last_login=now,
            date_joined=now,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)

        print(user)
        return user

    def create_user(self, email, first_name, last_name, phone_number, password, **extra_fields):

        return self._create_user(email, first_name, last_name, phone_number, password, False, False, **extra_fields)

    def create_superuser(self, email, first_name, last_name, phone_number, password, **extra_fields):
        user = self._create_user(email, first_name, last_name, phone_number, password, True, True, **extra_fields)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=254, unique=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    phone_number = models.CharField(verbose_name="Phone Number", max_length=24, unique=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)

    # come with django
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'

    # EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number']

    objects = MyUserManager()

    def __str__(self):
        return f"{self.email} ({self.first_name})"

    # def get_absolute_url(self):
    #     return "/users/%i/" % self.pk

