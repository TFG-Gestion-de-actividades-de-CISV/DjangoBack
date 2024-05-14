from django.db import models

# Create your models here.


class Activity(models.Model):
    name = models.CharField(max_length=254)
    adress = models.CharField(max_length=254)
    date_start = models.DateField()
    date_end = models.DateField()
    hours_start = models.CharField(max_length=254)
    price = models.CharField(max_length=254)
    packing_list = models.TextField()
    family_reunion = models.TextField()

    

