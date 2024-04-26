from django.contrib import admin
from .models import Web_User_Pending, Profile, User

# Register your models here.

admin.site.register(Web_User_Pending)

admin.site.register(Profile)

admin.site.register(User)