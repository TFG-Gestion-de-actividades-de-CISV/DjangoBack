from rest_framework import serializers
from .models import Web_User_Pending

class Web_User_Pending_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Web_User_Pending
        fields = "__all__"