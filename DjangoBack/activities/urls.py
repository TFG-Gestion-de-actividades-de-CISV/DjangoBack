from django.urls import path
from . import views

urlpatterns = [
    path("create_activity/", views.create_activity),
    path("all_activities", views.all_activities),
    path("ninos_inscription/", views.ninos_inscription),
    path("mayores_inscription/", views.mayores_inscription),
    path("lider_inscription/", views.lider_inscription),
    path("monitor_inscription/", views.monitor_inscription),
    path("get_or_create_inscription/<str:role>",
         views.get_or_create_inscription),
    path("all_inscriptions/<int:activity>", views.all_inscriptions),
    path("get_inscription/<int:activity>/<str:user_email>/<str:role>", views.get_inscription)


]
