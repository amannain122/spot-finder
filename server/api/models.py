from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db import models
from .managers import CustomUserManager, UserManager


USER_TYPE = (
    (0, 'Admin'),
    (1, 'User'),
)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(_('full name'), max_length=60, blank=True)
    last_name = models.CharField(_('full name'), max_length=60, blank=True)
    email = models.EmailField(_('email address'), unique=True)
    user_type = models.IntegerField(
        blank=True, default=USER_TYPE[1][0], choices=USER_TYPE)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    email_verified = models.BooleanField(
        default=True, verbose_name='email_verified')
    last_login = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name_plural = "All Users"

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if (self.user_type == 0):
            self.user_type = 0
            self.is_staff = True
            self.is_superuser = True

        elif (self.user_type == 1):
            self.user_type = 1
            self.is_staff = False
            self.is_superuser = False

        super(CustomUser, self).save(*args, **kwargs)

    def delete(self):
        super().delete()


class User(CustomUser):
    car_no_plate = models.CharField(max_length=1000, null=True, blank=True)

    objects = UserManager()

    class Meta:
        verbose_name_plural = "Users"

    def save(self, *args, **kwargs):
        self.user_type = 1
        self.is_staff = False
        self.is_superuser = False
        self.is_active = True

        super(User, self).save(*args, **kwargs)


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Coordinates(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f"Latitude: {self.latitude}, Longitude: {self.longitude}"


class Post(models.Model):
    class PostObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset()

    category = models.ForeignKey(Category, on_delete=models.PROTECT, default=1)
    coordinates = models.OneToOneField(Coordinates, on_delete=models.CASCADE)
    availability = models.CharField(max_length=20)
    type = models.CharField(max_length=20)
    capacity = models.IntegerField()
    available_space = models.IntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    time_restrictions = models.CharField(max_length=100)

    objects = models.Manager()  # default manager
    postobjects = PostObjects()  # custom manager

    def __str__(self):
        return f'{self.pk}'
