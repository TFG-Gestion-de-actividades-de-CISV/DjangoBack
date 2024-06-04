from rest_framework import serializers
from .models import *
import re


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = '__all__'


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
                  'pago']

    def validate_emergency_phone(self, value):
        if not re.match(r'^\+?[0-9]+$', value):
            raise serializers.ValidationError(
                "El teléfono solo puede contener números y puede comenzar con '+'.")
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
                  'pago']

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
                  'health_card', 'pago']

    def validate_emergency_phone(self, value):
        if not re.match(r'^\+?[0-9]+$', value):
            raise serializers.ValidationError(
                "El teléfono solo puede contener números y puede comenzar con '+'.")
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
                  't_shirt_size', 'medicines', 'health_card', 'pago']

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
                  "cisv_safeguarding", "health_card"]

    def validate_emergency_phone(self, value):
        if not re.match(r'^\+?[0-9]+$', value):
            raise serializers.ValidationError(
                "El teléfono solo puede contener números y puede comenzar con '+'.")
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
                  "cisv_safeguarding", "health_card"]

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
                  "t_shirt_size", "medicines", "sexual_crimes_certificate",
                  "criminal_offenses_certificate", "cisv_safeguarding", "health_card", "pago"]

    def validate_emergency_phone(self, value):
        if not re.match(r'^\+?[0-9]+$', value):
            raise serializers.ValidationError(
                "El teléfono solo puede contener números y puede comenzar con '+'.")
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
                  "cisv_safeguarding", "health_card", "pago"]

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
