from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('contact/', views.contact_view, name='contact'),
    path('about/', views.about_view, name='about'),
    path('licensing/', views.licensing_view, name='licensing'),
    path('privacy/', views.privacy_view, name='privacy'),
]