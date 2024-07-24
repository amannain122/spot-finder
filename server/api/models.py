from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, User
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


class Booking(models.Model):
    PARKING_LOT_CHOICES = [
        ('PL01', 'PL01'),
        ('PL02', 'PL02'),
        ('PL03', 'PL03'),
    ]
    PARKING_TIME_CHOICES = [
        (1, '1 hour'),
        (2, '2 hours'),
        (3, '3 hours'),
        (4, '4 hours'),
        (5, '5 hours'),
        (6, '6 hours'),
        (7, '7 hours'),
        (8, '8 hours'),
    ]

    BOOKING_STATUS_CHOICES = [
        ('booked', 'Booked'),
        ('canceled', 'Canceled'),
        ('expired', 'Expired'),
    ]
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    parking_id = models.CharField(max_length=10, choices=PARKING_LOT_CHOICES)
    parking_spot = models.CharField(max_length=10, unique=True)
    parking_charge = models.DecimalField(max_digits=10, decimal_places=2)
    parking_time = models.DateTimeField(default=timezone.now)
    booking_status = models.CharField(
        max_length=10, choices=BOOKING_STATUS_CHOICES, default='booked')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Booking by {self.user.email} for parking spot {self.parking_spot}s"

    # class Meta:
    #     unique_together = ('user', 'parking_spot')
