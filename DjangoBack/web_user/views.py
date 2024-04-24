from rest_framework.views import APIView
from rest_framework.response import Response 
from .serializer import Web_User_Pending_Serializer
from .models import Web_User_Pending
# Create your views here.

class Web_User_Pending_View(APIView):
    def post(self, request):
        print(request)
        serializer = Web_User_Pending_Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=200)
        return Response(status=400)

