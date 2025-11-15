from django.db import models
from datetime import timedelta
from django.utils import timezone

def one_day_from_now():
    return timezone.now().date() + timedelta(days=1)

# Create your models here.
class Task(models.Model):
    TaskID = models.AutoField(primary_key=True)
    Taskname = models.CharField(max_length=100)
    coinValue = models.PositiveIntegerField()

class User(models.Model):
    userID = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50)
    passwordhash = models.CharField(max_length=128)
    email = models.EmailField()
    userXP = models.PositiveIntegerField(default=0)
    coinBalance = models.PositiveIntegerField(default=100)

class DailyTask(models.Model):
    AssignmentID = models.AutoField(primary_key=True)
    TaskID = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='assignments')
    userID = models.ForeignKey(User, on_delete=models.CASCADE, related_name='daily_tasks')
    isCompleted = models.BooleanField(default=False)
    startDate = models.DateField(auto_now_add=True)
    expiryDate = models.DateField(default=one_day_from_now)

class StudySession(models.Model):
    SessionID = models.AutoField(primary_key=True)
    UserID = models.ForeignKey(User, on_delete=models.CASCADE, related_name='study_sessions')
    SubjectName = models.CharField(max_length=100)
    Study_Duration = models.DurationField()
    entryDate = models.DateField(auto_now_add=True)

class Avatar(models.Model):
    AvatarID = models.AutoField(primary_key=True)
    AvatarName = models.CharField(max_length=50)
    filename = models.CharField(max_length=255)
    cost = models.PositiveIntegerField()

class UserAvatar(models.Model):
    AvatarID = models.ForeignKey(Avatar, on_delete=models.CASCADE)
    UserID = models.ForeignKey(User, on_delete=models.CASCADE)
    class Meta:
        unique_together = ['AvatarID', 'UserID']

class Friends(models.Model):
    UserID = models.ForeignKey(User, related_name='friends', on_delete=models.CASCADE)
    FriendID = models.ForeignKey(User, related_name='friend_of', on_delete=models.CASCADE)
    DateAdded = models.DateField()

class LeaderboardEntry(models.Model):
    entryID = models.AutoField(primary_key=True)
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    rank = models.PositiveIntegerField()

class Challenges(models.Model):
    ChallengeID = models.AutoField(primary_key=True)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    isFull = models.BooleanField(default=False)
    MaxSize = models.PositiveIntegerField()
    CreatorID = models.ForeignKey(User, on_delete=models.CASCADE)
    ChallengeTitle = models.CharField(max_length=100)
    Status = models.CharField(max_length=20)
    goal = models.CharField(max_length=255)

class ChallengeParticipants(models.Model):
    UserID = models.ForeignKey(User, on_delete=models.CASCADE)
    ChallengeID = models.ForeignKey(Challenges, on_delete=models.CASCADE)
    joinDate = models.DateField(auto_now_add=True)
    progress =  models.PositiveIntegerField()
    class Meta:
        unique_together = ['UserID', 'ChallengeID']

class ChallengeLeaderboard(models.Model):
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    ChallengeID = models.ForeignKey(Challenges, on_delete=models.CASCADE)
    rank = models.PositiveIntegerField()
    class Meta:
        unique_together = ['userID', 'ChallengeID']
