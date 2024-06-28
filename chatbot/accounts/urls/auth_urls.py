from django.urls import path
from .. import views
from ..views import UserEditView, UserProfileEditView
from django.contrib.auth import views as auth_views

urlpatterns = [
    # path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    # path('register/', views.register_view.as_view(), name='register'),
    path('logout/', views.logout_view, name='logout'),
]