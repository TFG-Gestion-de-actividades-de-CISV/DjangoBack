from django.urls import path
from .views import Web_User_Pending_View


urlpatterns = [
    path("register/", Web_User_Pending_View.as_view())
]
