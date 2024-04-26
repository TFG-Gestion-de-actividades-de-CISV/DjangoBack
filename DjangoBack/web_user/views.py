from rest_framework.response import Response 
from rest_framework.authtoken.models import Token
from .serializer import Web_User_Pending_Serializer
from rest_framework.decorators import api_view
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import User


@api_view(['POST'])
def register(request):
    print(request.data)
    serializer = Web_User_Pending_Serializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.errors ,status=status.HTTP_201_CREATED, )
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):

    user = get_object_or_404(User, email=request.data["email"])
    
    if not user.check_password(request.data["password"]):
        return Response({"error": "Invalid password"}, status=status.HTTP_404_NOT_FOUND)

    token, created = Token.objects.get_or_create(user=user)
    is_admin = user.is_admin
    return Response({"token": token.key, "is_admin": is_admin}, status=status.HTTP_200_OK)


"""
class Web_User_Pending_View(APIView):
    def post(self, request):
        serializer = Web_User_Pending_Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=200)
        return Response(status=400)
"""


"""    
class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = make_password(request.data.get('password'))
        user = authenticate(email=email, password=password)
        print(password)
        if user is not None:
            token = Token.objects.get_or_create(user=user)
            return Response({"token": token.key, "is_admin": user.is_admin})
        else:
            return Response({"error": "Invalid login"}, status=400)
"""
