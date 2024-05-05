from rest_framework import serializers
import re
from .models import Web_User_Pending, Profile, User


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

    def validate_postal_code(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("El código postal solo puede contener números.")
        return value
    
    def validate_phone(self, value):
        if not re.match(r'^\+?[0-9]+$', value):
            raise serializers.ValidationError("El teléfono solo puede contener números y puede comenzar con '+'.")
        return value


class Web_User_Pending_Serializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = Web_User_Pending
        fields = ['email', 'password', 'is_admin', 'profile']

        

    def create(self, validated_data):
        profile_data = validated_data.pop("profile")
        profile = Profile.objects.create(**profile_data)
        web_user_pending = Web_User_Pending.objects.create(profile=profile, **validated_data)
        return web_user_pending


class Web_User_NoPassword_Serializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = Web_User_Pending
        fields = ['email' , 'profile']
