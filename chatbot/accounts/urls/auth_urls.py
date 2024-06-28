from django.urls import path
from .. import views
from ..views import UserEditView, UserProfileEditView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.register_view, name='register'),

    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('reset_password/', auth_views.PasswordResetView.as_view(
        template_name='auth/password_reset/password_reset.html',
        ), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(
        template_name='auth/password_reset/password_reset_done.html',
        ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        # template_name='auth/password_reset/password_reset_confirm.html',
        ), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='auth/password_reset/password_reset_complete.html',
        ), name='password_reset_complete'),
]