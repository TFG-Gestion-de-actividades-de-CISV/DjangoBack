from rest_framework import serializers
from .models import *
import re


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = '__all__'

    def validate(self, data):
        if data['date_start'] > data['date_end']:
            raise serializers.ValidationError("La fecha de inicio no puede ser posterior a la fecha de finalización.")
        return data
    
    def validate_price(self, value):
        try:
            float(value)
        except ValueError:
            raise serializers.ValidationError("El precio debe ser un número válido.")
        return value

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = "__all__"


class NinosSerializer(serializers.ModelSerializer):
    health_card = serializers.PrimaryKeyRelatedField(
        queryset=Document.objects.all())
    pago = serializers.PrimaryKeyRelatedField(queryset=Document.objects.all())

    class Meta:
        model = Nino
        fields = ["user", "activity", "rol", "allergy",
                  'image_authorization', 'emergency_phone',
                  't_shirt_size', 'medicines', 'health_card',
                  'pago', 'status']

    def validate_emergency_phone(self, value):
        if not re.match(r'^\+?[1-9]\d{1,14}$', value):
            raise serializers.ValidationError(
                "El teléfono debe estar en formato internacional. Solo puede contener números y, opcionalmente, un símbolo '+' al principio.")
        return value

    def create(self, validated_data):
        nino_instance = Nino.objects.create(**validated_data)
        return nino_instance


class NinosGetSerializer(serializers.ModelSerializer):
    health_card = serializers.SerializerMethodField()
    pago = serializers.SerializerMethodField()

    class Meta:
        model = Nino
        fields = ["allergy", 'image_authorization', 'emergency_phone',
                  't_shirt_size', 'medicines', 'health_card',
                  'pago', 'id', 'status']

    def get_health_card(self, obj):
        if obj.health_card:
            return self.context['request'].build_absolute_uri(obj.health_card.upload.url)
        return None

    def get_pago(self, obj):
        if obj.pago:
            return self.context['request'].build_absolute_uri(obj.pago.upload.url)
        return None


class MayoresSerializer(serializers.ModelSerializer):
    health_card = serializers.PrimaryKeyRelatedField(
        queryset=Document.objects.all())
    pago = serializers.PrimaryKeyRelatedField(queryset=Document.objects.all())

    class Meta:
        model = Mayor
        fields = ["user", "activity", "rol", "allergy",
                  'image_authorization', 'emergency_phone',
                  't_shirt_size', 'medicines',
                  'health_card', 'pago', 'status']

    def validate_emergency_phone(self, value):
        if not re.match(r'^\+?[1-9]\d{1,14}$', value):
            raise serializers.ValidationError(
                "El teléfono debe estar en formato internacional. Solo puede contener números y, opcionalmente, un símbolo '+' al principio.")
        return value

    def create(self, validated_data):
        mayor_instance = Mayor.objects.create(**validated_data)
        return mayor_instance


class MayoresGetSerializer(serializers.ModelSerializer):
    health_card = serializers.SerializerMethodField()
    pago = serializers.SerializerMethodField()

    class Meta:
        model = Mayor
        fields = ["allergy", 'image_authorization', 'emergency_phone',
                  't_shirt_size', 'medicines', 'health_card', 'pago', 'id', 'status']

    def get_health_card(self, obj):
        if obj.health_card:
            return self.context['request'].build_absolute_uri(obj.health_card.upload.url)
        return None

    def get_pago(self, obj):
        if obj.pago:
            return self.context['request'].build_absolute_uri(obj.pago.upload.url)
        return None


class LiderSerializer(serializers.ModelSerializer):
    sexual_crimes_certificate = serializers.PrimaryKeyRelatedField(
        queryset=Document.objects.all())
    criminal_offenses_certificate = serializers.PrimaryKeyRelatedField(
        queryset=Document.objects.all())
    cisv_safeguarding = serializers.PrimaryKeyRelatedField(
        queryset=Document.objects.all())
    health_card = serializers.PrimaryKeyRelatedField(
        queryset=Document.objects.all())

    class Meta:
        model = Lider
        fields = ["user", "activity", "rol", "dni", "allergy",
                  "profession", "languages", "first_aid",
                  "image_authorization", "emergency_phone",
                  "t_shirt_size", "medicines",
                  "sexual_crimes_certificate", "criminal_offenses_certificate",
                  "cisv_safeguarding", "health_card", 'status']

    def validate_dni(self, value):
        if not re.match(r'^\d{8}[A-Z]$', value) and not re.match(r'^[XYZ]\d{7}[A-Z]$', value):
            raise serializers.ValidationError(
            "El DNI/NIE no tiene un formato válido. Debe ser 8 dígitos seguidos de una letra (DNI) o una letra (X, Y, Z) seguida de 7 dígitos y una letra (NIE)."   
            )     
        return value


    def validate_emergency_phone(self, value):
        if not re.match(r'^\+?[1-9]\d{1,14}$', value):
            raise serializers.ValidationError(
                "El teléfono debe estar en formato internacional. Solo puede contener números y, opcionalmente, un símbolo '+' al principio.")
        return value

    def create(self, validated_data):
        lider_instance = Lider.objects.create(**validated_data)
        return lider_instance


class LiderGetSerializer(serializers.ModelSerializer):
    sexual_crimes_certificate = serializers.SerializerMethodField()
    criminal_offenses_certificate = serializers.SerializerMethodField()
    cisv_safeguarding = serializers.SerializerMethodField()
    health_card = serializers.SerializerMethodField()

    class Meta:
        model = Lider
        fields = ["dni",
                  "profession", "languages", "first_aid", "allergy",
                  "image_authorization", "emergency_phone",
                  "t_shirt_size", "medicines",
                  "sexual_crimes_certificate", "criminal_offenses_certificate",
                  "cisv_safeguarding", "health_card", 'id', 'status']

    def get_sexual_crimes_certificate(self, obj):
        if obj.sexual_crimes_certificate:
            return self.context['request'].build_absolute_uri(obj.sexual_crimes_certificate.upload.url)
        return None

    def get_criminal_offenses_certificate(self, obj):
        if obj.criminal_offenses_certificate:
            return self.context['request'].build_absolute_uri(obj.criminal_offenses_certificate.upload.url)
        return None

    def get_cisv_safeguarding(self, obj):
        if obj.cisv_safeguarding:
            return self.context['request'].build_absolute_uri(obj.cisv_safeguarding.upload.url)
        return None

    def get_health_card(self, obj):
        if obj.health_card:
            return self.context['request'].build_absolute_uri(obj.health_card.upload.url)
        return None


class MonitorSerializer(serializers.ModelSerializer):

    sexual_crimes_certificate = serializers.PrimaryKeyRelatedField(
        queryset=Document.objects.all())
    criminal_offenses_certificate = serializers.PrimaryKeyRelatedField(
        queryset=Document.objects.all())
    cisv_safeguarding = serializers.PrimaryKeyRelatedField(
        queryset=Document.objects.all())
    health_card = serializers.PrimaryKeyRelatedField(
        queryset=Document.objects.all())
    pago = serializers.PrimaryKeyRelatedField(queryset=Document.objects.all())

    class Meta:
        model = Monitor
        fields = ["user", "activity", "rol",  "allergy",
                  "dni", "languages",
                  "image_authorization", "emergency_phone",
                  "t_shirt_size", "medicines", "sexual_crimes_certificate", 'status',
                  "criminal_offenses_certificate", "cisv_safeguarding", "health_card", "pago"]

    def validate_emergency_phone(self, value):
        if not re.match(r'^\+?[1-9]\d{1,14}$', value):
            raise serializers.ValidationError(
                "El teléfono debe estar en formato internacional. Solo puede contener números y, opcionalmente, un símbolo '+' al principio.")
        return value

    def create(self, validated_data):
        monitor_instance = Monitor.objects.create(**validated_data)
        return monitor_instance


class MonitorGetSerializer(serializers.ModelSerializer):
    sexual_crimes_certificate = serializers.SerializerMethodField()
    criminal_offenses_certificate = serializers.SerializerMethodField()
    cisv_safeguarding = serializers.SerializerMethodField()
    health_card = serializers.SerializerMethodField()
    pago = serializers.SerializerMethodField()

    class Meta:
        model = Monitor
        fields = ["dni", "languages", "allergy",
                  "image_authorization", "emergency_phone",
                  "t_shirt_size", "medicines",
                  "sexual_crimes_certificate", "criminal_offenses_certificate",
                  "cisv_safeguarding", "health_card", "pago", 'id', 'status']

    def get_sexual_crimes_certificate(self, obj):
        if obj.sexual_crimes_certificate:
            return self.context['request'].build_absolute_uri(obj.sexual_crimes_certificate.upload.url)
        return None

    def get_criminal_offenses_certificate(self, obj):
        if obj.criminal_offenses_certificate:
            return self.context['request'].build_absolute_uri(obj.criminal_offenses_certificate.upload.url)
        return None

    def get_cisv_safeguarding(self, obj):
        if obj.cisv_safeguarding:
            return self.context['request'].build_absolute_uri(obj.cisv_safeguarding.upload.url)
        return None

    def get_health_card(self, obj):
        if obj.health_card:
            return self.context['request'].build_absolute_uri(obj.health_card.upload.url)
        return None

    def get_pago(self, obj):
        if obj.pago:
            return self.context['request'].build_absolute_uri(obj.pago.upload.url)
        return None


class InscripcionSerializer(serializers.ModelSerializer):
    
    user_name = serializers.SerializerMethodField()
    user_surnames = serializers.SerializerMethodField()
    user_email = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    activity_name = serializers.SerializerMethodField()


    class Meta:
        model = InscriptionBase
        fields = ["rol", "status", "user_name", "user_surnames", "id", "user_email", "activity_name"]
    
    def get_user_name(self, obj):
        return obj.user.profile.name if obj.user.profile else None
    
    def get_user_email(self, obj):
        return obj.user.email if obj.user.email else None
    
    
    def get_user_surnames(self, obj):
        return obj.user.profile.surnames if obj.user.profile else None
    
    def get_status(self, obj):
        return obj.get_status_display()
    
    def get_activity_name(self, obj):
        return obj.activity.name

class AllNinosFieldsSerializer(NinosGetSerializer):

    user_name = serializers.CharField(source='user.profile.name', read_only=True)
    user_surnames = serializers.CharField(source='user.profile.surnames', read_only=True)
    user_city = serializers.CharField(source='user.profile.city', read_only=True)
    user_postal_code = serializers.CharField(source='user.profile.postal_code', read_only=True)
    user_phone = serializers.CharField(source='user.profile.phone', read_only=True)
    user_birthdate = serializers.DateField(source='user.profile.birthdate', read_only=True)
    family_members_emails = serializers.SerializerMethodField()

    class Meta:
        model = Nino
        fields = NinosGetSerializer.Meta.fields + ["user_name", "user_surnames",
                            "user_city" , "user_postal_code", "user_phone", 
                            "user_birthdate", "family_members_emails"]
        

    def get_family_members_emails(self, obj):
        family_members = User.objects.filter(family=obj.user.family)
        return [member.email for member in family_members]

    

class AllMayoresFieldsSerializer(MayoresGetSerializer):
    
    user_name = serializers.CharField(source='user.profile.name', read_only=True)
    user_surnames = serializers.CharField(source='user.profile.surnames', read_only=True)
    user_city = serializers.CharField(source='user.profile.city', read_only=True)
    user_postal_code = serializers.CharField(source='user.profile.postal_code', read_only=True)
    user_phone = serializers.CharField(source='user.profile.phone', read_only=True)
    user_birthdate = serializers.DateField(source='user.profile.birthdate', read_only=True)
    family_members_emails = serializers.SerializerMethodField()

    class Meta:
        model = Mayor
        fields = MayoresGetSerializer.Meta.fields + ["user_name", "user_surnames",
                            "user_city" , "user_postal_code", "user_phone", "user_birthdate","family_members_emails"]

    def get_family_members_emails(self, obj):
        family_members = User.objects.filter(family=obj.user.family)
        return [member.email for member in family_members]


    
class AllLiderFieldsSerializer(LiderGetSerializer):
    
    user_name = serializers.CharField(source='user.profile.name', read_only=True)
    user_surnames = serializers.CharField(source='user.profile.surnames', read_only=True)
    user_city = serializers.CharField(source='user.profile.city', read_only=True)
    user_postal_code = serializers.CharField(source='user.profile.postal_code', read_only=True)
    user_phone = serializers.CharField(source='user.profile.phone', read_only=True)
    user_birthdate = serializers.DateField(source='user.profile.birthdate', read_only=True)
    family_members_emails = serializers.SerializerMethodField()

    class Meta:
        model = Lider
        fields = LiderGetSerializer.Meta.fields + ["user_name", "user_surnames",
                            "user_city" , "user_postal_code", "user_phone", "user_birthdate", "family_members_emails"]
    def get_family_members_emails(self, obj):
        family_members = User.objects.filter(family=obj.user.family)
        return [member.email for member in family_members]

    
class AllMonitorFieldsSerializer(MonitorGetSerializer):
    
    user_name = serializers.CharField(source='user.profile.name', read_only=True)
    user_surnames = serializers.CharField(source='user.profile.surnames', read_only=True)
    user_city = serializers.CharField(source='user.profile.city', read_only=True)
    user_postal_code = serializers.CharField(source='user.profile.postal_code', read_only=True)
    user_phone = serializers.CharField(source='user.profile.phone', read_only=True)
    user_birthdate = serializers.DateField(source='user.profile.birthdate', read_only=True)
    family_members_emails = serializers.SerializerMethodField()

    class Meta:
        model = Monitor 
        fields = MonitorGetSerializer.Meta.fields + ["user_name", "user_surnames",
                            "user_city" , "user_postal_code", "user_phone", "user_birthdate", "family_members_emails"]

    def get_family_members_emails(self, obj):
        family_members = User.objects.filter(family=obj.user.family)
        return [member.email for member in family_members]