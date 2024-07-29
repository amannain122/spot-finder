from django.contrib import admin
from .models import User, CustomUser, Booking

admin.site.register(User)
admin.site.register(Booking)
admin.site.register(CustomUser)
