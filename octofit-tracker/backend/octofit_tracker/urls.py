"""
octofit_tracker URL Configuration
"""

import os
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.decorators import api_view
from rest_framework.response import Response

from . import views

# Base URL for Codespaces REST API endpoints:
# https://$CODESPACE_NAME-8000.app.github.dev/api/

CODESPACE_NAME = os.environ.get("CODESPACE_NAME", "")

if CODESPACE_NAME:
    BASE_API_URL = f"https://{CODESPACE_NAME}-8000.app.github.dev/api/"
else:
    BASE_API_URL = "http://localhost:8000/api/"

router = DefaultRouter()
router.register(r"users", views.UserViewSet)
router.register(r"teams", views.TeamViewSet)
router.register(r"activities", views.ActivityViewSet)
router.register(r"leaderboard", views.LeaderboardViewSet)
router.register(r"workouts", views.WorkoutViewSet)

@api_view(["GET"])
def api_root(request, format=None):
    return Response({
        "users":       f"{BASE_API_URL}users/",
        "teams":       f"{BASE_API_URL}teams/",
        "activities":  f"{BASE_API_URL}activities/",
        "leaderboard": f"{BASE_API_URL}leaderboard/",
        "workouts":    f"{BASE_API_URL}workouts/",
    })

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api_root, name="api-root"),
    path("api/", include(router.urls)),
]
