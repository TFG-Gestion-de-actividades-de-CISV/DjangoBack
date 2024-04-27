from rest_framework.response import Response 
from rest_framework.authtoken.models import Token
from .serializer import Web_User_Pending_Serializer
from rest_framework.decorators import api_view
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import User
from django.http import JsonResponse



@api_view(['POST'])
def register(request):
    serializer = Web_User_Pending_Serializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.errors ,status=status.HTTP_201_CREATED, )
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    user = get_object_or_404(User, email=request.data["email"])
    
    if not user.check_password(request.data["password"]):
        return JsonResponse({"error" : "Invalif password"}, status=status.HTTP_404_NOT_FOUND)
    
    token, created = Token.objects.get_or_create(user=user)
    is_admin = user.is_admin
    response = JsonResponse({"is_admin": is_admin})
    #Guarda token en las cookies
    response.set_cookie("token", token.key, httponly=True)
    
    return response


