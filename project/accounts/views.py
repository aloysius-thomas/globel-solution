from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render

from accounts.forms import LoginForm
from solutions.forms import ClientRequestForm
from solutions.models import Service


def home(request):
    return render(request, 'home.html', {'form': ClientRequestForm()})


@login_required
def dashboard(request):
    projects = Service.objects.all().order_by('-id')[:5]
    return render(request, 'dashboard.html', {'projects': projects})


def about(request):
    return render(request, 'about.html', {})


def logout_view(request):
    logout(request)
    return redirect('home')


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('dashboard')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def software_development_page_view(request):
    return render(request, 'services/software-development.html', {})


def digital_marketing_page_view(request):
    return render(request, 'services/digital-marketing.html', {})


def mobile_development_page_view(request):
    return render(request, 'services/mobile-development.html', {})


def project_support_page_view(request):
    return render(request, 'services/project-support.html', {})


def contact_us_page_view(request):
    return render(request, 'services/contact-us.html', {})
