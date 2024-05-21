from rest_framework import	serializers
from .models import Activity, Ninos


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = '__all__'


class NinosSerializer(serializers.ModelSerializer):
    class Meta:
        model= Ninos
        fields = ["user", "activity", "rol", "allergy",
            'cisv_authorization', 'emergency_phone',
            't_shirt_size', 'medicines']
        
        
        def create(self, validated_data):
            nino_instance = Ninos.objects.create(**validated_data)
            return nino_instance
        

class NinosGetSerializer(serializers.ModelSerializer):
    class Meta:
        model= Ninos
        fields = [ "allergy",'cisv_authorization', 'emergency_phone',
            't_shirt_size', 'medicines']
    