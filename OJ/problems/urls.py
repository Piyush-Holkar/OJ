from django.urls import path
from . import views

urlpatterns = [
    path("", views.problems, name="problems"),
    path("<int:problem_id>/", views.problem, name="problem"),
    path("create/", views.create, name="create"),
    path("submissions/", views.submissions, name="submissions"),
    path("submissions/<int:submission_id>/", views.submission, name="submission"),
]
