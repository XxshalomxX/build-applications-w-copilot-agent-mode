from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from djongo import models
from octofit_tracker import settings
from pymongo import MongoClient

# Modelos simples para ejemplo, se recomienda definir modelos reales en models.py
class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    class Meta:
        app_label = 'octofit_tracker'

class Activity(models.Model):
    name = models.CharField(max_length=100)
    user_email = models.EmailField()
    team = models.CharField(max_length=100)
    class Meta:
        app_label = 'octofit_tracker'

class Leaderboard(models.Model):
    user_email = models.EmailField()
    team = models.CharField(max_length=100)
    points = models.IntegerField()
    class Meta:
        app_label = 'octofit_tracker'

class Workout(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    class Meta:
        app_label = 'octofit_tracker'

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        User = get_user_model()
        # Conexión directa para crear índice único en email
        client = MongoClient('mongodb://localhost:27017')
        db = client['octofit_db']
        db.users.drop()
        db.teams.drop()
        db.activities.drop()
        db.leaderboard.drop()
        db.workouts.drop()
        db.users.create_index([('email', 1)], unique=True)

        # Equipos
        teams = [
            {'name': 'Marvel'},
            {'name': 'DC'}
        ]
        db.teams.insert_many(teams)

        # Usuarios
        users = [
            {'email': 'tony@marvel.com', 'name': 'Tony Stark', 'team': 'Marvel'},
            {'email': 'steve@marvel.com', 'name': 'Steve Rogers', 'team': 'Marvel'},
            {'email': 'bruce@dc.com', 'name': 'Bruce Wayne', 'team': 'DC'},
            {'email': 'clark@dc.com', 'name': 'Clark Kent', 'team': 'DC'}
        ]
        db.users.insert_many(users)

        # Actividades
        activities = [
            {'name': 'Running', 'user_email': 'tony@marvel.com', 'team': 'Marvel'},
            {'name': 'Cycling', 'user_email': 'steve@marvel.com', 'team': 'Marvel'},
            {'name': 'Swimming', 'user_email': 'bruce@dc.com', 'team': 'DC'},
            {'name': 'Boxing', 'user_email': 'clark@dc.com', 'team': 'DC'}
        ]
        db.activities.insert_many(activities)

        # Leaderboard
        leaderboard = [
            {'user_email': 'tony@marvel.com', 'team': 'Marvel', 'points': 100},
            {'user_email': 'steve@marvel.com', 'team': 'Marvel', 'points': 90},
            {'user_email': 'bruce@dc.com', 'team': 'DC', 'points': 95},
            {'user_email': 'clark@dc.com', 'team': 'DC', 'points': 85}
        ]
        db.leaderboard.insert_many(leaderboard)

        # Workouts
        workouts = [
            {'name': 'Push Ups', 'description': 'Do 3 sets of 15 reps.'},
            {'name': 'Sit Ups', 'description': 'Do 3 sets of 20 reps.'}
        ]
        db.workouts.insert_many(workouts)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
