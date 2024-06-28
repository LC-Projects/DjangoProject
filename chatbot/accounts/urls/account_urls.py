from django.urls import path
from .. import views
from ..views import UserEditView, UserProfileEditView
from django.contrib.auth import views as auth_views

urlpatterns = [    
    path('edit_user/', UserEditView.as_view(), name='edit_user'),
    path('edit_profile/', UserProfileEditView.as_view(), name='edit_profile'),
]