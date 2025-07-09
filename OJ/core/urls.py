from django.urls import path
from . import views

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("profile/<str:username>/", views.profile, name="profile"),
    path("ai/", views.AI, name="ai"),
]
