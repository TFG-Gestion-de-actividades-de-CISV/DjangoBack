from rest_framework.response import Response 
from rest_framework.decorators import api_view, authentication_classes
from .serializer import ActivitySerializer
from rest_framework import status
from web_user.authentication import CookieTokenAuthentication
from .models import Activity




# Create your views here.
@api_view(["POST"])
@authentication_classes([CookieTokenAuthentication])
def create_activity(request):

    if not request.user.is_authenticated:
        return Response({"error": "NO autenticado"}, status=status.HTTP_403_FORBIDDEN)
    
    if not request.user.is_admin:
        return Response({"error": "No es admin"}, status= status.HTTP_403_FORBIDDEN)



    serializer = ActivitySerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response({'status': 'success'},status=status.HTTP_201_CREATED)
    return Response({"Error": serializer.errors},status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@authentication_classes([CookieTokenAuthentication])
def all_activities(request):

    if not request.user.is_authenticated:
        return Response({"error": "NO autenticado"}, status=status.HTTP_403_FORBIDDEN)
    
    activities = Activity.objects.all()

    serializer = ActivitySerializer(activities, many = True)

    return Response(serializer.data, status=status.HTTP_200_OK)