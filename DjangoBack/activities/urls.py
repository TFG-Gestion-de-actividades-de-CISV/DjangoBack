from django.urls import path
from . import views

urlpatterns = [
    path("create_activity/", views.create_activity),
    path("all_activities", views.all_activities),
    path("ninos_inscription/", views.ninos_inscription),
    path("get_or_create_inscription/<str:role>", views.get_or_create_inscription)


]