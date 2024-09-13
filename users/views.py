from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.views import View
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth import logout
from disease.models import ProductImage

def index_view(request):
    return render(request, 'index.html')


def about_view(request):
    return render(request, 'about.html')

def emergency_view(request):
    return render(request, 'emergency-care.html')

def avoid_view(request):
    return render(request, 'foods-to-avoid.html')


def info_view(request):
    return render(request, 'info.html')

def selfcare_view(request):
    return render(request, 'selfcare.html')

def symptoms_view(request):
    return render(request, 'symptoms.html')


def triggers_view(request):
    return render(request, 'triggers.html')



class UserRegisterView(View):
    def get(self, request):
        form = UserRegistrationForm()
        return render(request, 'users/register.html', {'form': form})

    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        return render(request, 'users/register.html', {'form': form})


class UserLoginView(View):
    def get(self, request):
        form = UserLoginForm()
        return render(request, 'users/login.html', {'form': form})

    def post(self, request):
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('home') 
        return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


def user_images(request):
    images = ProductImage.objects.filter(user=request.user)
    return render(request, 'users/scanned.html', {'images': images})