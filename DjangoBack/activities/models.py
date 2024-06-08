from django.db import IntegrityError, models
from django.forms import ValidationError
from web_user.models import User

# Create your models here.


class Document(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    upload = models.FileField()

    def __str__(self):
        return self.upload.url


class Activity(models.Model):
    name = models.CharField(max_length=254)
    adress = models.CharField(max_length=254)
    date_start = models.DateField()
    date_end = models.DateField()
    hours_start = models.CharField(max_length=254)
    price = models.CharField(max_length=254)
    packing_list = models.TextField()
    family_reunion = models.TextField()
    there_are_meting = models.BooleanField(default=False)



class InscriptionBase(models.Model):

    STATUS_CHOICES = ((0, "Pendiente"), (1,"Aceptado"), (2, "Rechazado"))
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    rol = models.CharField(max_length=20)
    allergy = models.TextField(blank=True, null=True)
    status = models.SmallIntegerField(choices=STATUS_CHOICES)

    class Meta:
        unique_together = ("user", "activity")

    def save(self, *args, **kwargs):
        try:
            super(InscriptionBase, self).save(*args, **kwargs)
        except IntegrityError:
            raise ValidationError(
                "Ya existe una inscripción para este usuario y actividad.")


class Participantes(InscriptionBase):
    health_card = models.ForeignKey(Document, on_delete=models.CASCADE,
                                    related_name='health_card')
    image_authorization = models.BooleanField(default=False)
    emergency_phone = models.CharField(max_length=20)
    t_shirt_size = models.CharField(max_length=10)
    medicines = models.TextField(blank=True, null=True)
    pago = models.ForeignKey(Document, on_delete=models.CASCADE,
                             related_name='pago')


class Nino(Participantes):
    pass


class Mayor(Participantes):
    pass


class Colaborador(InscriptionBase):
    sexual_crimes_certificate = models.ForeignKey(Document, on_delete=models.CASCADE,
                                                  related_name='sexual_crimes_certificate')
    criminal_offenses_certificate = models.ForeignKey(Document, on_delete=models.CASCADE,
                                                      related_name='criminal_offenses_certificate')
    cisv_safeguarding = models.ForeignKey(Document, on_delete=models.CASCADE,
                                          related_name='cisv_safeguarding')


class Lider(Colaborador):
    dni = models.CharField(max_length=9)
    profession = models. CharField(max_length=100)
    languages = models.TextField()
    first_aid = models.BooleanField(default=False)

    health_card = models.ForeignKey(Document, on_delete=models.CASCADE,
                                    related_name='lider_health_card')
    image_authorization = models.BooleanField(default=False)
    emergency_phone = models.CharField(max_length=20)
    t_shirt_size = models.CharField(max_length=10)
    medicines = models.TextField(blank=True, null=True)


class Monitor(Colaborador):
    dni = models.CharField(max_length=9)
    languages = models.CharField(max_length=100)

    health_card = models.ForeignKey(Document, on_delete=models.CASCADE,
                                    related_name='monitor_health_card')
    image_authorization = models.BooleanField(default=False)
    emergency_phone = models.CharField(max_length=20)
    t_shirt_size = models.CharField(max_length=10)
    medicines = models.TextField(blank=True, null=True)
    pago = models.ForeignKey(Document, on_delete=models.CASCADE,
                             related_name='monitor_pago')
