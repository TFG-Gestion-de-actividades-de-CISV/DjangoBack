from django.db import IntegrityError, models
from django.forms import ValidationError
from web_user.models import User

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

    
class InscriptionBase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    rol = models.CharField(max_length=20)
    allergy = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ("user", "activity")

    def save(self, *args, **kwargs):
        try:
            super(InscriptionBase, self).save(*args, **kwargs)
        except IntegrityError:
            raise ValidationError("Ya existe una inscripción para este usuario y actividad.")

class Participantes(InscriptionBase):
    # health_card = models.CharField(max_length=255, blank=True, null=True)
    cisv_authorization = models.BooleanField(default=False)
    emergency_phone = models.CharField(max_length=20)
    t_shirt_size = models.CharField(max_length=10, blank=True, null=True)
    medicines = models.TextField()
    #pago


class Nino(Participantes):
    pass

class Mayor(Participantes):
    pass

class Colaborador(InscriptionBase):
    #sexual_crimes_certificate = models.FileField(upload_to='certificados/')
    #criminal_crimes_certificate = models.FileField(upload_to='certificados/')
    # CISV Safeguarding
    pass

class Lider(Colaborador):
    dni = models.CharField(max_length=9)
    profession = models. CharField(max_length=100)
    languages = models.CharField(max_length=100)
    first_aid = models.BooleanField(default=False)

    # health_card = models.CharField(max_length=255, blank=True, null=True)
    cisv_authorization = models.BooleanField(default=False)
    emergency_phone = models.CharField(max_length=20)
    t_shirt_size = models.CharField(max_length=10, blank=True, null=True)
    medicines = models.TextField()

class Monitor(Colaborador):
    dni = models.CharField(max_length=9)
    languages = models.CharField(max_length=100)

     # health_card = models.CharField(max_length=255, blank=True, null=True)
    cisv_authorization = models.BooleanField(default=False)
    emergency_phone = models.CharField(max_length=20)
    t_shirt_size = models.CharField(max_length=10, blank=True, null=True)
    medicines = models.TextField()
    #pago