from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

from .views import UserEditView, UserProfileEditView, ChangePasswordView

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register_view, name='register'),

    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),


    path('edit_user/', UserEditView.as_view(), name='edit_user'),
    path('edit_profile/', UserProfileEditView.as_view(), name='edit_profile'),
    path('edit_mood/', views.edit_mood, name='edit_mood'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('password/', ChangePasswordView.as_view(), name='set_password'),
]
