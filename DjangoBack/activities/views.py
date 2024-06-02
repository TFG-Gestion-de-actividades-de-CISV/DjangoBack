from django.forms import ValidationError
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes
from .serializer import *
from rest_framework import status
from web_user.authentication import CookieTokenAuthentication
from .models import *


# Create your views here.
@api_view(["POST"])
@authentication_classes([CookieTokenAuthentication])
def create_activity(request):

    if not request.user.is_authenticated:
        return Response({"error": "NO autenticado"}, status=status.HTTP_403_FORBIDDEN)

    if not request.user.is_admin:
        return Response({"error": "No es admin"}, status=status.HTTP_403_FORBIDDEN)

    serializer = ActivitySerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response({'status': 'success'}, status=status.HTTP_201_CREATED)
    return Response({"Error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@authentication_classes([CookieTokenAuthentication])
def all_activities(request):

    if not request.user.is_authenticated:
        return Response({"error": "NO autenticado"}, status=status.HTTP_403_FORBIDDEN)

    activities = Activity.objects.all().order_by('-id')

    serializer = ActivitySerializer(activities, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@authentication_classes([CookieTokenAuthentication])
def ninos_inscription(request):

    if not request.user.is_authenticated:
        return Response({"error": "NO autenticado"}, status=status.HTTP_403_FORBIDDEN)

    health_card = request.FILES.get('health_card')
    pago = request.FILES.get('pago')

    data = request.data.copy()
    data["user"] = request.user.id
    data["rol"] = "ninos"

    if health_card is None:
        last_inscription = Nino.objects.filter(
            user=request.user.id).order_by('-id').first()
        data["health_card"] = last_inscription.health_card.id
    else:
        health_card_instance = Document.objects.create(upload=health_card)
        data["health_card"] = health_card_instance.id

    if pago is None:
        last_inscription = Nino.objects.filter(
            user=request.user.id).order_by('-id').first()
        data["pago"] = last_inscription.pago.id
    else:
        pago_instance = Document.objects.create(upload=pago)
        data["pago"] = pago_instance.id

    serializer = NinosSerializer(data=data)

    if serializer.is_valid():
        try:

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({"error": e}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


serializers_dict = {
    'ninos': NinosGetSerializer,
    'mayores': MayoresGetSerializer,
    'lider': LiderGetSerializer,
    'monitor': MonitorGetSerializer
}

models_dict = {
    'ninos': Nino,
    'mayores': Mayor,
    'lider': Lider,
    'monitor': Monitor
}


@api_view(["GET"])
@authentication_classes([CookieTokenAuthentication])
def get_or_create_inscription(request, role):

    if not request.user.is_authenticated:
        return Response({"error": "NO autenticado"}, status=status.HTTP_403_FORBIDDEN)

    user = request.user

    model_class = models_dict.get(role)
    if not model_class:
        return Response({"error", "Rol no válido"}, status=status.HTTP_400_BAD_REQUEST)

    inscription = model_class.objects.filter(user=user).last()

    if inscription:
        serializer_class = serializers_dict.get(role)
        if serializer_class:
            serializer = serializer_class(
                inscription, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Rol no válido"}, status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response({}, status=status.HTTP_200_OK)


@api_view(["POST"])
@authentication_classes([CookieTokenAuthentication])
def mayores_inscription(request):

    if not request.user.is_authenticated:
        return Response({"error": "NO autenticado"}, status=status.HTTP_403_FORBIDDEN)

    health_card = request.FILES.get('health_card')
    pago = request.FILES.get('pago')

    data = request.data
    data["user"] = request.user.id
    data["rol"] = "mayores"

    if health_card is None:
        last_inscription = Mayor.objects.filter(
            user=request.user.id).order_by('-id').first()
        data["health_card"] = last_inscription.health_card.id
    else:
        health_card_instance = Document.objects.create(upload=health_card)
        data["health_card"] = health_card_instance.id

    if pago is None:
        last_inscription = Mayor.objects.filter(
            user=request.user.id).order_by('-id').first()
        data["pago"] = last_inscription.pago.id
    else:
        pago_instance = Document.objects.create(upload=pago)
        data["pago"] = pago_instance.id

    serializer = MayoresSerializer(data=data)

    if serializer.is_valid():
        try:

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({"error": e}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@authentication_classes([CookieTokenAuthentication])
def lider_inscription(request):

    if not request.user.is_authenticated:
        return Response({"error": "NO autenticado"}, status=status.HTTP_403_FORBIDDEN)

    sexual_crimes_certificate = request.FILES.get('sexual_crimes_certificate')
    criminal_offenses_certificate = request.FILES.get(
        'criminal_offenses_certificate')
    health_card = request.FILES.get('health_card')
    cisv_safeguarding = request.FILES.get('cisv_safeguarding')

    data = request.data
    data["user"] = request.user.id
    data["rol"] = "lider"

    if health_card is None:
        last_inscription = Lider.objects.filter(
            user=request.user.id).order_by('-id').first()
        data["health_card"] = last_inscription.health_card.id
    else:
        health_card_instance = Document.objects.create(upload=health_card)
        data["health_card"] = health_card_instance.id

    if sexual_crimes_certificate is None:
        last_inscription = Lider.objects.filter(
            user=request.user.id).order_by('-id').first()
        data["sexual_crimes_certificate"] = last_inscription.sexual_crimes_certificate.id
    else:
        sexual_crimes_certificate_instance = Document.objects.create(
            upload=sexual_crimes_certificate)
        data["sexual_crimes_certificate"] = sexual_crimes_certificate_instance.id

    if criminal_offenses_certificate is None:
        last_inscription = Lider.objects.filter(
            user=request.user.id).order_by('-id').first()
        data["criminal_offenses_certificate"] = last_inscription.criminal_offenses_certificate.id
    else:
        criminal_offenses_certificate_instance = Document.objects.create(
            upload=criminal_offenses_certificate)
        data["criminal_offenses_certificate"] = criminal_offenses_certificate_instance.id

    if cisv_safeguarding is None:
        last_inscription = Lider.objects.filter(
            user=request.user.id).order_by('-id').first()
        data["cisv_safeguarding"] = last_inscription.cisv_safeguarding.id
    else:
        cisv_safeguarding_instance = Document.objects.create(
            upload=cisv_safeguarding)
        data["cisv_safeguarding"] = cisv_safeguarding_instance.id

    serializer = LiderSerializer(data=data)

    if serializer.is_valid():
        try:

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({"error": e}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@authentication_classes([CookieTokenAuthentication])
def monitor_inscription(request):
    sexual_crimes_certificate = request.FILES.get('sexual_crimes_certificate')
    criminal_offenses_certificate = request.FILES.get(
        'criminal_offenses_certificate')
    health_card = request.FILES.get('health_card')
    cisv_safeguarding = request.FILES.get('cisv_safeguarding')
    pago = request.FILES.get('pago')

    if not request.user.is_authenticated:
        return Response({"error": "NO autenticado"}, status=status.HTTP_403_FORBIDDEN)

    data = request.data
    data["user"] = request.user.id
    data["rol"] = "monitor"

    if health_card is None:
        last_inscription = Monitor.objects.filter(
            user=request.user.id).order_by('-id').first()
        data["health_card"] = last_inscription.health_card.id
    else:
        health_card_instance = Document.objects.create(upload=health_card)
        data["health_card"] = health_card_instance.id

    if pago is None:
        last_inscription = Monitor.objects.filter(
            user=request.user.id).order_by('-id').first()
        data["pago"] = last_inscription.pago.id
    else:
        pago_instance = Document.objects.create(upload=pago)
        data["pago"] = pago_instance.id

    if sexual_crimes_certificate is None:
        last_inscription = Monitor.objects.filter(
            user=request.user.id).order_by('-id').first()
        data["sexual_crimes_certificate"] = last_inscription.sexual_crimes_certificate.id
    else:
        sexual_crimes_certificate_instance = Document.objects.create(
            upload=sexual_crimes_certificate)
        data["sexual_crimes_certificate"] = sexual_crimes_certificate_instance.id

    if criminal_offenses_certificate is None:
        last_inscription = Monitor.objects.filter(
            user=request.user.id).order_by('-id').first()
        data["criminal_offenses_certificate"] = last_inscription.criminal_offenses_certificate.id
    else:
        criminal_offenses_certificate_instance = Document.objects.create(
            upload=criminal_offenses_certificate)
        data["criminal_offenses_certificate"] = criminal_offenses_certificate_instance.id

    if cisv_safeguarding is None:
        last_inscription = Monitor.objects.filter(
            user=request.user.id).order_by('-id').first()
        data["cisv_safeguarding"] = last_inscription.cisv_safeguarding.id
    else:
        cisv_safeguarding_instance = Document.objects.create(
            upload=cisv_safeguarding)
        data["cisv_safeguarding"] = cisv_safeguarding_instance.id

    serializer = MonitorSerializer(data=data)

    if serializer.is_valid():
        try:

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({"error": e}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
