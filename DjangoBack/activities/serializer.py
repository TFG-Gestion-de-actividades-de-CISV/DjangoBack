from rest_framework import	serializers
from .models import Activity, Nino, Mayor, Lider, Monitor
import re



class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = '__all__'


class NinosSerializer(serializers.ModelSerializer):
    class Meta:
        model= Nino
        fields = ["user", "activity", "rol", "allergy",
            'cisv_authorization', 'emergency_phone',
            't_shirt_size', 'medicines']
        

    def validate_emergency_phone(self, value):
        if not re.match(r'^\+?[0-9]+$', value):
            raise serializers.ValidationError("El teléfono solo puede contener números y puede comenzar con '+'.")
        return value
        
    def create(self, validated_data):
        nino_instance = Nino.objects.create(**validated_data)
        return nino_instance
        

class NinosGetSerializer(serializers.ModelSerializer):
    class Meta:
        model= Nino
        fields = [ "allergy",'cisv_authorization', 'emergency_phone',
            't_shirt_size', 'medicines']


class MayoresSerializer(serializers.ModelSerializer):
    class Meta:
        model= Mayor
        fields = ["user", "activity", "rol", "allergy",
            'cisv_authorization', 'emergency_phone',
            't_shirt_size', 'medicines']
        
    def validate_emergency_phone(self, value):
        if not re.match(r'^\+?[0-9]+$', value):
            raise serializers.ValidationError("El teléfono solo puede contener números y puede comenzar con '+'.")
        return value
        
    def create(self, validated_data):
        mayor_instance = Mayor.objects.create(**validated_data)
        return mayor_instance
        

class MayoresGetSerializer(serializers.ModelSerializer):
    class Meta:
        model= Mayor
        fields = [ "allergy",'cisv_authorization', 'emergency_phone',
            't_shirt_size', 'medicines']
        


class LiderSerializer(serializers.ModelSerializer):
    class Meta:
        model= Lider
        fields = ["user", "activity", "rol", "dni", "allergy",
                  "profession", "languages", "first_aid",
                  "cisv_authorization", "emergency_phone", 
                  "t_shirt_size", "medicines"]
        
        
    def validate_emergency_phone(self, value):
        if not re.match(r'^\+?[0-9]+$', value):
            raise serializers.ValidationError("El teléfono solo puede contener números y puede comenzar con '+'.")
        return value
        
    def create(self, validated_data):
        lider_instance = Lider.objects.create(**validated_data)
        return lider_instance
        

class LiderGetSerializer(serializers.ModelSerializer):
    class Meta:
        model= Lider
        fields = [ "dni", 
                  "profession", "languages", "first_aid", "allergy",
                  "cisv_authorization", "emergency_phone", 
                  "t_shirt_size", "medicines"]
        

class MonitorSerializer(serializers.ModelSerializer):
    class Meta:
        model= Monitor
        fields = ["user", "activity", "rol",  "allergy",
                  "dni", "languages",
                  "cisv_authorization", "emergency_phone", 
                  "t_shirt_size", "medicines"]
        
    def validate_emergency_phone(self, value):
        if not re.match(r'^\+?[0-9]+$', value):
            raise serializers.ValidationError("El teléfono solo puede contener números y puede comenzar con '+'.")
        return value
        

    def create(self, validated_data):
        monitor_instance = Monitor.objects.create(**validated_data)
        return monitor_instance
        

class MonitorGetSerializer(serializers.ModelSerializer):
    class Meta:
        model= Monitor
        fields = [ "dni", "languages", "allergy",
                  "cisv_authorization", "emergency_phone", 
                  "t_shirt_size", "medicines"]