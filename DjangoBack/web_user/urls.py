from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register),
    path("login/", views.login),
    path("registration_requests", views.registration_requests),
    path("reject_request/", views.reject_request),
    path("acept_request/", views.acept_request),
    path("change_password/", views.change_password)

]
