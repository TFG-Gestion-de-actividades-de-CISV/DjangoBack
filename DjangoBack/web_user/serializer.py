from rest_framework import serializers
from .models import Web_User_Pending, Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['name', 'surname', 'second_surname', 'city', 'postal_code', 'phone', 'birthdate']


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

