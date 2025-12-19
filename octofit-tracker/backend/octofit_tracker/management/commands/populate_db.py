import os
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.decorators import api_view
from rest_framework.response import Response

from . import views

router = DefaultRouter()
router.register(r"users", views.UserViewSet, basename="user")
router.register(r"teams", views.TeamViewSet, basename="team")
router.register(r"activities", views.ActivityViewSet, basename="activity")
router.register(r"leaderboard", views.LeaderboardViewSet, basename="leaderboard")
router.register(r"workouts", views.WorkoutViewSet, basename="workout")

# Base de la API usando el nombre del Codespace
CODESPACE_NAME = os.environ.get("CODESPACE_NAME", "")

if CODESPACE_NAME:
    BASE_API_URL = f"https://{CODESPACE_NAME}-8000.app.github.dev/api/"
else:
    # Fallback cuando corres local
    BASE_API_URL = "http://localhost:8000/api/"

@api_view(["GET"])
def api_root(request, format=None):
    # Usamos siempre BASE_API_URL (requisito del ejercicio)
    base_url = BASE_API_URL
    return Response({
        "users":       f"{base_url}users/",
        "teams":       f"{base_url}teams/",
        "activities":  f"{base_url}activities/",
        "leaderboard": f"{base_url}leaderboard/",
        "workouts":    f"{base_url}workouts/",
    })

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api_root, name="api-root"),
    path("api/", include(router.urls)),
]
