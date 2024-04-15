from django.db import models
from django.contrib.auth.hashers import make_password

# Usuario pendiente de aceptación de admin
class Web_User_Pending(models.Model):
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=254)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        self.password =make_password(self.password)
        super().save(*args, **kwargs)
