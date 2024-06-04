from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.db import models


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('email address required'))

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('user_type', 0)
        extra_fields.setdefault('email_verified', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must be assigned to is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(
                _('Superuser must be assigned to is_superuser=True.'))
        if extra_fields.get('user_type') != 0:
            raise ValueError(_('Superuser must have user_type of admin.'))
        return self.create_user(email, password, **extra_fields)


class UserManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(user_type=1)
