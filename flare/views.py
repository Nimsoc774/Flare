from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from .models import User
from django.http import HttpResponse

@login_required(login_url='login')
def home(request):
    return HttpResponse("Project 'flare' is working!")

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            from django.contrib import messages
            messages.error(request, 'Invalid username or password.')
    
    return render(request,'Flare/login.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Password is automatically hashed
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('login')  # Redirect to login page
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = CustomUserCreationForm()
        
    return render(request,'Flare/registration.html',{'form': form})
