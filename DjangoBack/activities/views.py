from rest_framework.response import Response 
from rest_framework.decorators import api_view, authentication_classes
from .serializer import ActivitySerializer
from rest_framework import status
from web_user.authentication import CookieTokenAuthentication




# Create your views here.
@api_view(["POST"])
@authentication_classes([CookieTokenAuthentication])
def create_activity(request):
    serializer = ActivitySerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response({'status': 'success'},status=status.HTTP_201_CREATED)
    return Response({"Error": serializer.errors},status=status.HTTP_400_BAD_REQUEST)
