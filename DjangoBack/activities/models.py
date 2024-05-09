from django.db import models

# Create your models here.


class Activity(models.Model):
    name = models.CharField(max_length=254, null=True)
    adress = models.CharField(max_length=254, null=True)
    date_start = models.DateField(null=True)
    date_end = models.DateField(null=True)
    hours_start = models.CharField(max_length=254, null=True)
    price = models.CharField(max_length=254, null=True)
    packing_list = models.CharField(max_length=1023, null=True)
    family_reunion = models.CharField(max_length=1023, null=True)

    

