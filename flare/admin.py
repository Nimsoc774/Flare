from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    User, Task, DailyTask, StudySession, Avatar, 
    UserAvatar, Friends, LeaderboardEntry, Challenges, 
    ChallengeParticipants, ChallengeLeaderboard
)
from .forms import CustomUserCreationForm, CustomUserChangeForm


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Admin interface for custom User model"""
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ['id', 'username', 'email', 'user_xp', 'coin_balance', 'is_staff']
    list_filter = ('is_staff', 'is_active', 'date_joined')
    search_fields = ('username', 'email')
    ordering = ('-date_joined',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('email', 'first_name', 'last_name')}),
        ('Custom Fields', {'fields': ('user_xp', 'coin_balance')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'coin_value']
    search_fields = ['name']


@admin.register(DailyTask)
class DailyTaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'task', 'is_completed', 'start_date', 'expiry_date']
    list_filter = ['is_completed', 'start_date']
    search_fields = ['user__username', 'task__name']
    readonly_fields = ['start_date']


@admin.register(StudySession)
class StudySessionAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'subject_name', 'study_duration', 'entry_date']
    search_fields = ['user__username', 'subject_name']
    readonly_fields = ['entry_date']


@admin.register(Avatar)
class AvatarAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'filename', 'cost']
    search_fields = ['name']


@admin.register(UserAvatar)
class UserAvatarAdmin(admin.ModelAdmin):
    list_display = ['user', 'avatar']
    search_fields = ['user__username', 'avatar__name']


@admin.register(Friends)
class FriendsAdmin(admin.ModelAdmin):
    list_display = ['user', 'friend', 'date_added']
    search_fields = ['user__username', 'friend__username']


@admin.register(LeaderboardEntry)
class LeaderboardEntryAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'rank']
    search_fields = ['user__username']
    list_filter = ['rank']


@admin.register(Challenges)
class ChallengesAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'creator', 'status', 'start_date', 'end_date', 'is_full']
    list_filter = ['status', 'is_full', 'start_date']
    search_fields = ['title', 'creator__username']


@admin.register(ChallengeParticipants)
class ChallengeParticipantsAdmin(admin.ModelAdmin):
    list_display = ['user', 'challenge', 'progress', 'join_date']
    search_fields = ['user__username', 'challenge__title']
    list_filter = ['join_date']


@admin.register(ChallengeLeaderboard)
class ChallengeLeaderboardAdmin(admin.ModelAdmin):
    list_display = ['user', 'challenge', 'rank']
    search_fields = ['user__username', 'challenge__title']
    list_filter = ['rank']