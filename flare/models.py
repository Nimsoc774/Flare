from django.db import models
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

def one_day_from_now():
    return timezone.now().date() + timedelta(days=1)

# Create your models here.

class User(AbstractUser):
    
    user_xp= models.PositiveIntegerField(default=0)
    coin_balance = models.PositiveIntegerField(default=100)
    
    class Meta:
        db_table = 'auth_user'
    
    def __str__(self):
        return self.username

class Task(models.Model):
    name = models.CharField(max_length=100)
    coin_value = models.PositiveIntegerField()
    
    def __str__(self):
        return self.name


class DailyTask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='assignments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='daily_tasks')
    is_completed = models.BooleanField(default=False)
    start_date = models.DateField(auto_now_add=True)
    expiry_date = models.DateField(default=one_day_from_now)
    
    def __str__(self):
        return f"{self.user.username} - {self.task.name}"


class StudySession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='study_sessions')
    subject_name = models.CharField(max_length=100)
    study_duration = models.DurationField()
    entry_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.subject_name}"


class Avatar(models.Model):
    name = models.CharField(max_length=50)
    filename = models.CharField(max_length=255)
    cost = models.PositiveIntegerField()
    
    def __str__(self):
        return self.name


class UserAvatar(models.Model):
    avatar = models.ForeignKey(Avatar, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ['avatar', 'user']
    
    def __str__(self):
        return f"{self.user.username} - {self.avatar.name}"


class Friends(models.Model):
    user = models.ForeignKey(User, related_name='friends', on_delete=models.CASCADE)
    friend = models.ForeignKey(User, related_name='friend_of', on_delete=models.CASCADE)
    date_added = models.DateField()
    
    class Meta:
        unique_together = ['user', 'friend']
    
    def __str__(self):
        return f"{self.user.username} - {self.friend.username}"


class LeaderboardEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rank = models.PositiveIntegerField()
    
    def __str__(self):
        return f"{self.user.username} - Rank {self.rank}"


class Challenges(models.Model):
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    is_full = models.BooleanField(default=False)
    max_size = models.PositiveIntegerField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    status = models.CharField(max_length=20)
    goal = models.CharField(max_length=255)
    
    def __str__(self):
        return self.title


class ChallengeParticipants(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenges, on_delete=models.CASCADE)
    join_date = models.DateField(auto_now_add=True)
    progress = models.PositiveIntegerField()
    
    class Meta:
        unique_together = ['user', 'challenge']
    
    def __str__(self):
        return f"{self.user.username} - {self.challenge.title}"


class ChallengeLeaderboard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenges, on_delete=models.CASCADE)
    rank = models.PositiveIntegerField()
    
    class Meta:
        unique_together = ['user', 'challenge']
    
    def __str__(self):
        return f"{self.user.username} - {self.challenge.title} Rank {self.rank}"