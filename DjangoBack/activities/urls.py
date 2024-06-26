from django.urls import path
from . import views

urlpatterns = [
    path("create_activity/", views.create_activity, name='create_activity'),
    path("all_activities", views.all_activities, name='all_activities'),
    path("ninos_inscription/", views.ninos_inscription, name='ninos_inscription'),
    path("mayores_inscription/", views.mayores_inscription, name='mayores_inscription'),
    path("lider_inscription/", views.lider_inscription, name='lider_inscription'),
    path("monitor_inscription/", views.monitor_inscription, name='monitor_inscription'),
    path("parent_inscription/", views.parent_inscription, name='parent_inscription'),

    path("get_or_create_inscription/<str:role>",
         views.get_or_create_inscription, name=''),
    path("all_inscriptions/<int:activity>", views.all_inscriptions, name='all_inscriptions'),
    path("get_inscription/<int:activity>/<str:user_email>/<str:role>", views.get_inscription, name='get_inscription'),
    path('accept_inscription/<int:inscription_id>/', views.accept_inscription, name='accept_inscription'),
    path('reject_inscription/<int:inscription_id>/', views.reject_inscription, name='reject_inscription'),
    path('user_inscriptions', views.user_inscriptions, name='user_inscriptions'),
    path("update_activity/<int:activity_id>/", views.update_activity, name="update_activity"),
    path("get_activity/<int:activity_id>/", views.get_activity, name="get_activity"),
    path("delete_activity/<int:activity_id>/", views.delete_activity, name="delete_activity"),


]
