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
    activity = models.ForeignKey(Activity, on_delete=models.SET_NULL, null = True)
    rol = models.CharField(max_length=20)
    allergy = models.TextField(blank=True, null=True)
    status = models.SmallIntegerField(choices=STATUS_CHOICES)
    visible = models.BooleanField(default=True)  # Nuevo campo para controlar la visibilidad


    class Meta:
        unique_together = ("user", "activity")

    def save(self, *args, **kwargs):
        try:
            super(InscriptionBase, self).save(*args, **kwargs)
        except IntegrityError:
            raise ValidationError(
                "Ya existe una inscripción para este usuario y actividad.")


class Participantes(InscriptionBase):
    health_card = models.ForeignKey(Document, on_delete=models.SET_NULL, null=True,
                                    related_name='health_card')
    image_authorization = models.BooleanField(default=False)
    emergency_phone = models.CharField(max_length=20)
    t_shirt_size = models.CharField(max_length=10)
    medicines = models.TextField(blank=True, null=True)
    pago = models.ForeignKey(Document, on_delete=models.SET_NULL, null=True,
                             related_name='pago')

    def delete(self, *args, **kwargs):
        otros_participantes_salud = Participantes.objects.exclude(id=self.id).filter(health_card=self.health_card)
        if not otros_participantes_salud.exists():
            self.health_card.delete()

        otros_participantes_pago = Participantes.objects.exclude(id=self.id).filter(pago=self.pago)
        if not otros_participantes_pago.exists():
            self.pago.delete()

        super(Participantes, self).delete(*args, **kwargs)

class Nino(Participantes):
    pass


class Mayor(Participantes):
    pass


class Colaborador(InscriptionBase):
    sexual_crimes_certificate = models.ForeignKey(Document, on_delete=models.SET_NULL, null=True,
                                                  related_name='sexual_crimes_certificate')
    criminal_offenses_certificate = models.ForeignKey(Document, on_delete=models.SET_NULL, null=True,
                                                      related_name='criminal_offenses_certificate')
    cisv_safeguarding = models.ForeignKey(Document, on_delete=models.SET_NULL, null=True,
                                          related_name='cisv_safeguarding')

    def delete(self, *args, **kwargs):
        otros_colaboradores_sexual = Colaborador.objects.exclude(id=self.id).filter(sexual_crimes_certificate=self.sexual_crimes_certificate)
        if not otros_colaboradores_sexual.exists():
            self.sexual_crimes_certificate.delete()

        otros_colaboradores_criminal = Colaborador.objects.exclude(id=self.id).filter(criminal_offenses_certificate=self.criminal_offenses_certificate)
        if not otros_colaboradores_criminal.exists():
            self.criminal_offenses_certificate.delete()

        otros_colaboradores_cisv = Colaborador.objects.exclude(id=self.id).filter(cisv_safeguarding=self.cisv_safeguarding)
        if not otros_colaboradores_cisv.exists():
            self.cisv_safeguarding.delete()

        super(Colaborador, self).delete(*args, **kwargs)

class Lider(Colaborador):
    dni = models.CharField(max_length=9)
    profession = models. CharField(max_length=100)
    languages = models.TextField()
    first_aid = models.BooleanField(default=False)

    health_card = models.ForeignKey(Document, on_delete=models.SET_NULL, null=True,
                                    related_name='lider_health_card')
    image_authorization = models.BooleanField(default=False)
    emergency_phone = models.CharField(max_length=20)
    t_shirt_size = models.CharField(max_length=10)
    medicines = models.TextField(blank=True, null=True)

    def delete(self, *args, **kwargs):
        otros_lideres_salud = Lider.objects.exclude(id=self.id).filter(health_card=self.health_card)
        if not otros_lideres_salud.exists():
            self.health_card.delete()

        otros_lideres_pago = Lider.objects.exclude(id=self.id).filter(pago=self.pago)
        if not otros_lideres_pago.exists():
            self.pago.delete()

        super(Lider, self).delete(*args, **kwargs)


class Monitor(Colaborador):
    dni = models.CharField(max_length=9)
    languages = models.CharField(max_length=100)

    health_card = models.ForeignKey(Document, on_delete=models.SET_NULL, null=True,
                                    related_name='monitor_health_card')
    image_authorization = models.BooleanField(default=False)
    emergency_phone = models.CharField(max_length=20)
    t_shirt_size = models.CharField(max_length=10)
    medicines = models.TextField(blank=True, null=True)
    pago = models.ForeignKey(Document, on_delete=models.SET_NULL, null=True,
                             related_name='monitor_pago')

    def delete(self, *args, **kwargs):
        otros_monitores_salud = Monitor.objects.exclude(id=self.id).filter(health_card=self.health_card)
        if not otros_monitores_salud.exists():
            self.health_card.delete()

        otros_monitores_pago = Monitor.objects.exclude(id=self.id).filter(pago=self.pago)
        if not otros_monitores_pago.exists():
            self.pago.delete()

        super(Monitor, self).delete(*args, **kwargs)