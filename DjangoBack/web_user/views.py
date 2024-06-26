from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializer import *
from rest_framework.decorators import api_view, authentication_classes
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import User, Web_User_Pending, Profile
from django.http import JsonResponse
from .authentication import CookieTokenAuthentication
from django.contrib.auth.hashers import check_password, make_password


@api_view(['POST'])
def register(request):

    user_data = request.data

    # Si no hay usuarios en el sistema, crear el primer usuario como administrador
    if not User.objects.exists():
        user_data["is_admin"] = True
        user_serializer = User_Serializer(data=user_data)
        if user_serializer.is_valid():
            password = user_data.pop("password")
            user = user_serializer.save()
            user.set_password(password)
            user.save()
            return Response(user_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"Error": user_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    # Si ya hay usuarios en el sistema, crear una solicitud pendiente
    serializer = Web_User_Pending_Serializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED, )
    return Response({"Error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):

    if Web_User_Pending.objects.filter(email=request.data["email"]).exists():
        return Response({"error": "La petición de registro aun no ha sido evaluada"}, status=status.HTTP_403_FORBIDDEN)


    user = get_object_or_404(User, email=request.data["email"])
    if not user.check_password(request.data["password"]):
        return JsonResponse({"error": "Invalid password"}, status=status.HTTP_404_NOT_FOUND)

    token, created = Token.objects.get_or_create(user=user)
    is_admin = user.is_admin
    response = JsonResponse({"is_admin": is_admin})
    # Guarda token en las cookies
    response.set_cookie("token", token.key, httponly=True,  samesite='Lax')

    return response


@api_view(["POST"])
@authentication_classes([CookieTokenAuthentication])
def logout(request):
    # Elimina token de BD

    if not request.user.is_authenticated:
        return Response({"error": "Usuario no autenticado"}, status=status.HTTP_403_FORBIDDEN)

    request.user.auth_token.delete()

    response = Response({"message": "Logout exitoso"},
                        status=status.HTTP_200_OK)
    response.delete_cookie("token")
    return response


@api_view(['GET'])
@authentication_classes([CookieTokenAuthentication])
def registration_requests(request):

    if not request.user.is_authenticated:
        return Response({"error": "NO autenticado"}, status=status.HTTP_403_FORBIDDEN)
    user = request.user

    if not user.is_admin:
        return Response({"error": "No es admin"}, status=status.HTTP_403_FORBIDDEN)

    regist_requests = Web_User_Pending.objects.all()

    serializer = Web_User_NoPassword_Serializer(regist_requests, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([CookieTokenAuthentication])
def reject_request(request):

    if not request.user.is_authenticated:
        return Response({"error": "NO autenticado"}, status=status.HTTP_403_FORBIDDEN)
    user = request.user

    if not user.is_admin:
        return Response({"error": "No es admin"}, status=status.HTTP_403_FORBIDDEN)

    email = request.data["email"]
    print(request.data["reason"])
    try:
        web_user_pending = Web_User_Pending.objects.get(email=email)
        web_user_pending.delete()
        return Response({'status': 'success'}, status=status.HTTP_200_OK)
    except Web_User_Pending.DoesNotExist:
        return Response({"error": "Peticion no existe"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@authentication_classes([CookieTokenAuthentication])
def acept_request(request):
    if not request.user.is_authenticated:
        return Response({"error": "NO autenticado"}, status=status.HTTP_403_FORBIDDEN)
    user = request.user

    if not user.is_admin:
        return Response({"error": "No es admin"}, status=status.HTTP_403_FORBIDDEN)

    email = request.data["email"]

    try:
        web_user_pending = Web_User_Pending.objects.get(email=email)

        # Creamos nuevo profile

        new_profile = Profile.objects.create(
            name=web_user_pending.profile.name,
            surnames=web_user_pending.profile.surnames,
            city=web_user_pending.profile.city,
            postal_code=web_user_pending.profile.postal_code,
            phone=web_user_pending.profile.phone,
            birthdate=web_user_pending.profile.birthdate
        )


        # Creamos nuevo user
        new_user = User.objects.create_user(
            email=email,
            profile=new_profile,
            password=None
        )
        # Añadir a la familia
        family_member_email = web_user_pending.family_member_email
        if family_member_email:
            family_member = User.objects.get(email=family_member_email)
            new_user.family = family_member.family
        if not new_user.family:
            new_user.family = Family.objects.create()
        
    
        new_user.password = web_user_pending.password
        new_user.save()

        web_user_pending.delete()
        return Response({'status': 'success'}, status=status.HTTP_201_CREATED)
    except Web_User_Pending.DoesNotExist:
        return Response({"error": "Peticion no existe"}, status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])
@authentication_classes([CookieTokenAuthentication])
def change_password(request):

    if not request.user.is_authenticated:
        return Response({"error": "NO autenticado"}, status=status.HTTP_403_FORBIDDEN)
    
    user = request.user

   
    if not check_password(request.data["password_old"], user.password):
        return Response({"error": "Contraseña actual incorrecta"}, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(request.data["password_new"])
    user.save()
    return Response({'status': 'success'}, status=status.HTTP_200_OK)


@api_view(["GET"])
@authentication_classes([CookieTokenAuthentication])
def info_profile(request):

    if not request.user.is_authenticated:
        return Response({"error": "NO autenticado"}, status=status.HTTP_403_FORBIDDEN)
    user = request.user

    profile = user.profile
    serializer = User_Profile_Serializer(profile)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["PUT"])
@authentication_classes([CookieTokenAuthentication])
def update_profile(request):

    if not request.user.is_authenticated:
        return Response({"error": "NO autenticado"}, status=status.HTTP_403_FORBIDDEN)

    user = request.user
    profile = user.profile

    serializer = User_Profile_Update_Serializer(
        profile, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response({'status': 'success'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
