from django.forms import ValidationError
from rest_framework.response import Response 
from rest_framework.decorators import api_view, authentication_classes
from .serializer import ActivitySerializer, NinosSerializer, NinosGetSerializer
from rest_framework import status
from web_user.authentication import CookieTokenAuthentication
from .models import Activity, InscriptionBase, Ninos




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


@api_view(["POST"])
@authentication_classes([CookieTokenAuthentication])
def ninos_inscription(request):
    
    if not request.user.is_authenticated:
        return Response({"error": "NO autenticado"}, status=status.HTTP_403_FORBIDDEN)
    

    data = request.data
    data["user"] = request.user.id
    data["rol"] = "ninos"

    serializer = NinosSerializer(data=data)
    
    if serializer.is_valid():
        try:

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({"error": e}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

serializers_dict = {
    'ninos': NinosGetSerializer
}

models_dict = {
    'ninos': Ninos
}

@api_view(["GET"])
@authentication_classes([CookieTokenAuthentication])
def get_or_create_inscription(request, role):

    if not request.user.is_authenticated:
        return Response({"error": "NO autenticado"}, status=status.HTTP_403_FORBIDDEN)
    


    user = request.user

    model_class = models_dict.get(role)
    if not model_class:
        return Response({"errro", "Rol no válido"}, status=status.HTTP_400_BAD_REQUEST)
    
    inscription = model_class.objects.filter(user=user).first()

    if inscription:
        serializer_class = serializers_dict.get(role)
        if serializer_class:
            serializer = serializer_class(inscription)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Rol no válido"}, status=status.HTTP_400_BAD_REQUEST)
    
    else:
        Response({}, status=status.HTTP_200_OK)

   