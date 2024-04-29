from rest_framework.response import Response 
from rest_framework.authtoken.models import Token
from .serializer import Web_User_Pending_Serializer, Web_User_NoPassword_Serializer
from rest_framework.decorators import api_view, authentication_classes
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import User, Web_User_Pending
from django.http import JsonResponse
from .authentication import CookieTokenAuthentication



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
    response.set_cookie("token", token.key, httponly=True, samesite=None,secure=True)
    print(response.cookies)

    return response

@api_view(['GET'])
@authentication_classes([CookieTokenAuthentication])
def registration_requests(request):

    if not request.user.is_authenticated:
        return Response({"error": "NO autenticado"}, status=status.HTTP_403_FORBIDDEN)
    user = request.user
    
    if not user.is_admin:
        return Response({"error": "No es admin"}, status= status.HTTP_403_FORBIDDEN)

    regist_requests = Web_User_Pending.objects.all()

    serializer = Web_User_NoPassword_Serializer(regist_requests, many = True)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([CookieTokenAuthentication])
def reject_request(request):
    
    if not request.user.is_authenticated:
        return Response({"error": "NO autenticado"}, status=status.HTTP_403_FORBIDDEN)
    user = request.user
    
    if not user.is_admin:
        return Response({"error": "No es admin"}, status= status.HTTP_403_FORBIDDEN)
    
    email = request.data["email"]
    print(request.data["reason"])
    try:
        web_user_pending = Web_User_Pending.objects.get(email = email)
        web_user_pending.delete()
        return Response({'status': 'success'},status=status.HTTP_200_OK)
    except Web_User_Pending.DoesNotExist:
        return Response({"error": "Peticion no existe"},status=status.HTTP_404_NOT_FOUND)

