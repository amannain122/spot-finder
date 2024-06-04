from django.contrib import admin
from .models import Coordinates, Post, Category, User


admin.site.register(User)
admin.site.register(Coordinates)
admin.site.register(Post)
admin.site.register(Category)
