from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register, name='register'),
    path("login/", views.login, name='login'),
    path("registration_requests/", views.registration_requests, name='registration_requests'),
    path("reject_request/", views.reject_request, name='reject_request'),
    path("acept_request/", views.acept_request, name='acept_request'),
    path("change_password/", views.change_password, name='change_password'),
    path("logout/", views.logout, name='logout')

]
