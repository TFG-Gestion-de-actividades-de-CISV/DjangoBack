from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser


class Profile(models.Model):
    name = models.TextField(max_length=50)

# Usuario pendiente de aceptación de admin
class Web_User_Pending(models.Model):
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=254)
    is_admin = models.BooleanField(default=False)

    profile = models.OneToOneField(Profile, on_delete=models.CASCADE,null=True, blank=True)

    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        self.password =make_password(self.password)
        super().save(*args, **kwargs)

'''''

class Custom_User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE,null=True, blank=True)

    def save(self, *args, **kwargs):
        self.username=self.email
        super().save(*args, **kwargs)

'''''