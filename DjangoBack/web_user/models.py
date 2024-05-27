from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager


class Profile(models.Model):
    name = models.CharField(max_length=254)
    surnames = models.CharField(max_length=254)
    city = models.CharField(max_length=254)
    postal_code = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    birthdate = models.DateField()
    

# Usuario pendiente de aceptación de admin
class Web_User_Pending(models.Model):
    email = models.EmailField(max_length=254, unique=True, error_messages={"unique": "El email ya está en uso."})
    password = models.CharField(max_length=254)
    is_admin = models.BooleanField(default=False)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        self.password =make_password(self.password)
        super().save(*args, **kwargs)



class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_admin = models.BooleanField(default=False)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE,null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        self.username=self.email
        super().save(*args, **kwargs)
