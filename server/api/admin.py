from django.contrib import admin
from .models import Coordinates, Post, Category, User, Booking


admin.site.register(User)
admin.site.register(Coordinates)
admin.site.register(Post)
admin.site.register(Booking)
admin.site.register(Category)
