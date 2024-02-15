from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .decorators import unauthenticated_user, allowed_users, admin_only
from .forms import CreateUserForm

@login_required(login_url='login')
@admin_only
def dashboard(request):
    return render(request, 'users/dashboard.html')

@unauthenticated_user
def doctorLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')

    return render(request, 'users/login.html')

@unauthenticated_user
def signup(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')

    context = {'form': form}
    return render(request, 'users/signup.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

def userPage(request):
    return render(request, 'users/user.html')

@allowed_users(allowed_roles=['doctor'])
def doctorDashboard(request):
    return render(request, 'users/doctor/doctor_dashboard.html')

@allowed_users(allowed_roles=['patient'])
def patientDashboard(request):
    return render(request, 'users/patient/patient_dashboard.html')

@allowed_users(allowed_roles=['staff'])
def staffDashboard(request):    
    return render(request, 'users/staff/staff_dashboard.html')