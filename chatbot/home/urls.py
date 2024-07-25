from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('lobby/', views.lobby_view, name='lobby'),
    path('about/', views.about_view, name='about'),
    path('licensing/', views.licensing_view, name='licensing'),
    path('privacy/', views.privacy_view, name='privacy'),
]