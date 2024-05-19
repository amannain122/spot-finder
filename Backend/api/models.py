from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


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