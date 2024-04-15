from rest_framework import viewsets
from .serializer import Web_User_Pending_Serializer
from .models import Web_User_Pending
# Create your views here.

class Web_User_Pending_View(viewsets.ModelViewSet):
    serializer_class = Web_User_Pending_Serializer
    queryset = Web_User_Pending.objects.all()