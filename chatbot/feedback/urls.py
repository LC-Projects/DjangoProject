from django.urls import path, include
from . import views

urlpatterns = [
    path("list/", views.FeedbackFilterView.as_view(), name="home"),
    path("detail/<int:pk>/", views.FeedbackDetailView.as_view(), name="feedback_detail"),
    path('contact/', views.FeedbackView.as_view(), name='contact'),
]
