from django.urls import path, include
from rest_framework import routers
from .views import Web_User_Pending_View


router = routers.DefaultRouter()
router.register(r'user_pending', Web_User_Pending_View)

urlpatterns = [
    path("", include(router.urls))
]
