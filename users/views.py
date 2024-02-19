from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from .decorators import unauthenticated_user, allowed_users, admin_only
from .forms import CreateUserForm

@login_required(login_url='login')
@admin_only
def dashboard(request):
    return render(request, 'users/dashboard.html')

@unauthenticated_user
def userLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')

    return render(request, 'users/login.html')

@unauthenticated_user
def userSignup(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='patient')
            user.groups.add(group)
            return redirect('login')

    context = {'form': form}
    return render(request, 'users/signup.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

def userPage(request):
    return render(request, 'users/user.html')


# Doctor login, signup, dashboard, profile, update profile, delete profile
def doctorLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('doctor-dashboard')

    return render(request, 'users/doctor/doctor_login.html')

def doctorLogout(request):
    logout(request)
    return redirect('landing-page')

def doctorProfile(request):
    return render(request, 'users/doctor/doctor_profile.html')

def doctorUpdateProfile(request):
    return render(request, 'users/doctor/doctor_update_profile.html')

def doctorDeleteProfile(request):
    return render(request, 'users/doctor/doctor_delete_profile.html')

# Patient login, signup, dashboard, profile, update profile, delete profile
def patientLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('patient-dashboard')

    return render(request, 'users/patient/patient_login.html')

def patientSignup(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='patient')
            user.groups.add(group)
            return redirect('patient-login')

    context = {'form': form}
    return render(request, 'users/patient/patient_signup.html', context)

def patientLogout(request):
    logout(request)
    return redirect('landing-page')

def patientDashboard(request):
    return render(request, 'users/patient/patient_dashboard.html')

def patientGuidelines(request):
    return render(request, 'users/patient/patient_guide.html')

def patientProfile(request):
    return render(request, 'users/patient/patient_profile.html')

def patientUpdateProfile(request):
    return render(request, 'users/patient/patient_update_profile.html')

def patientDeleteProfile(request):
    return render(request, 'users/patient/patient_delete_profile.html')


# Staff login, signup, dashboard, profile, update profile, delete profile
def staffLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('staff-dashboard')

    return render(request, 'users/staff/staff_login.html')

def staffLogout(request):  
    logout(request)
    return redirect('landing-page')

def staffDashboard(request):
    return render(request, 'users/staff/staff_dashboard.html')

def staffProfile(request):
    return render(request, 'users/staff/staff_profile.html')

def staffUpdateProfile(request):    

    return render(request, 'users/staff/staff_update_profile.html')

def staffDeleteProfile(request):
    return render(request, 'users/staff/staff_delete_profile.html')

@login_required(login_url='login')
@allowed_users(allowed_roles=['doctor'])
def doctorDashboard(request):
    return render(request, 'users/doctor/doctor_dashboard.html')

@login_required(login_url='login')
@allowed_users(allowed_roles=['patient'])
def patientDashboard(request):
    return render(request, 'users/patient/patient_dashboard.html')

@login_required(login_url='login')
@allowed_users(allowed_roles=['staff'])
def staffDashboard(request):    
    return render(request, 'users/staff/staff_dashboard.html')

def landingPage(request):
    return render(request, 'users/landing_page.html')