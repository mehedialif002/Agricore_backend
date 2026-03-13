from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

REGISTRATION_CHOICES = [
    ('email', 'Email'),
    ('google', 'Google')
]

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('customer', 'Customer'),
    )

    email               = models.EmailField(unique=True)
    first_name          = models.CharField(max_length=30, default='', null=True, blank=True)
    last_name           = models.CharField(max_length=30, default='', null=True, blank=True)
    registration_method = models.CharField(max_length=20, choices=REGISTRATION_CHOICES, default='email')
    is_staff            = models.BooleanField(default=False)
    is_superuser        = models.BooleanField(default=False)
    is_active           = models.BooleanField(default=True) 
    is_verified         = models.BooleanField(default=True)  # ✅ True — সরাসরি active
    date_joined         = models.DateTimeField(auto_now_add=True)
    role                = models.CharField(max_length=10, choices=ROLE_CHOICES, default='customer')

    objects        = CustomUserManager()
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"