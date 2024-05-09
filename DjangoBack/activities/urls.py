from django.urls import path
from . import views

urlpatterns = [
    path("create_activity/", views.create_activity),
    path("all_activities", views.all_activities)


]