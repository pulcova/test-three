from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.auth.models import User


from .decorators import unauthenticated_user, allowed_users, admin_only
from .forms import CreateUserForm, PatientUpdateForm, StaffUpdateForm, DoctorUpdateForm
from .models import Patient, Doctor, Staff

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

def landingPage(request):
    return render(request, 'users/landing_page.html')


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

@login_required(login_url='doctor-login')
@allowed_users(allowed_roles=['doctor'])
def doctorProfile(request):
    doctor = Doctor.objects.get(user=request.user)
    context = {'doctor': doctor}
    return render(request, 'users/doctor/doctor_profile.html', context)

@login_required(login_url='doctor-login')
@allowed_users(allowed_roles=['doctor'])
def doctorUpdateProfile(request):
    doctor = Doctor.objects.get(user=request.user)
    form = DoctorUpdateForm(instance=doctor)

    if request.method == 'POST':
        form = DoctorUpdateForm(request.POST, request.FILES, instance=doctor)
        if form.is_valid():
            form.save()
            return redirect('doctor-profile')
    
    context = {'form': form, 'doctor': doctor}
    return render(request, 'users/doctor/doctor_update_profile.html', context)

@login_required(login_url='doctor-login')
@allowed_users(allowed_roles=['doctor'])
def doctorDeleteProfile(request):
    doctor = Doctor.objects.get(user=request.user)

    if request.method == 'POST':
        doctor.user.delete()
        return redirect('landing-page')
    
    context = {'doctor': doctor}
    return render(request, 'users/doctor/doctor_delete_profile.html', context)

@login_required(login_url='doctor-login')
@allowed_users(allowed_roles=['doctor'])
def doctorDashboard(request):
    doctor = Doctor.objects.get(user=request.user)

    context = {'doctor': doctor}
    return render(request, 'users/doctor/doctor_dashboard.html', context)

@login_required(login_url='doctor-login')
@allowed_users(allowed_roles=['doctor'])
def staffList(request):
    staff = Staff.objects.all()

    context = {'staff': staff}
    return render(request, 'users/doctor/doctor_staff_list.html', context)


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
            Patient.objects.create( user=user )
            return redirect('patient-login')

    context = {'form': form}
    return render(request, 'users/patient/patient_signup.html', context)

def patientLogout(request):
    logout(request)
    return redirect('landing-page')

@login_required(login_url='patient-login')
@allowed_users(allowed_roles=['patient'])
def patientDashboard(request):
    return render(request, 'users/patient/patient_dashboard.html')

@login_required(login_url='patient-login')
@allowed_users(allowed_roles=['patient'])
def patientGuidelines(request):
    return render(request, 'users/patient/patient_guide.html')

@login_required(login_url='patient-login')
@allowed_users(allowed_roles=['patient'])
def patientProfile(request):
    patient = Patient.objects.get(user=request.user)
    context = {'patient': patient}
    return render(request, 'users/patient/patient_profile.html', context)

@login_required(login_url='patient-login')
@allowed_users(allowed_roles=['patient'])
def patientUpdateProfile(request):
    patient = Patient.objects.get(user=request.user)
    form = PatientUpdateForm(instance=patient)
    
    if request.method == 'POST':
        form = PatientUpdateForm(request.POST, request.FILES, instance=patient)
        if form.is_valid():
            form.save()
            return redirect('patient-profile')

    context = {'form': form, 'patient': patient}
    return render(request, 'users/patient/patient_update_profile.html', context)

@login_required(login_url='patient-login')
@allowed_users(allowed_roles=['patient'])
def patientDeleteProfile(request):
    patient = Patient.objects.get(user=request.user)
    
    if request.method == 'POST':
        patient.user.delete()
        return redirect('landing-page')
    
    context = {'patient': patient}
    return render(request, 'users/patient/patient_delete_profile.html', context)

@login_required(login_url='patient-login')
@allowed_users(allowed_roles=['patient'])
def patientDashboard(request):
    patient = Patient.objects.get(user=request.user)

    context = {'patient': patient}
    return render(request, 'users/patient/patient_dashboard.html', context)

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

@login_required(login_url='staff-login')
@allowed_users(allowed_roles=['staff'])
def staffDashboard(request):
    return render(request, 'users/staff/staff_dashboard.html')

@login_required(login_url='staff-login')
@allowed_users(allowed_roles=['staff'])
def staffProfile(request):
    staff = Staff.objects.get(user=request.user)
    context = {'staff': staff}
    return render(request, 'users/staff/staff_profile.html', context)

@login_required(login_url='staff-login')
@allowed_users(allowed_roles=['staff'])
def staffUpdateProfile(request):    
    staff = Staff.objects.get(user=request.user)
    form = StaffUpdateForm(instance=staff)

    if request.method == 'POST':
        form = StaffUpdateForm(request.POST, request.FILES, instance=staff)
        if form.is_valid():
            form.save()
            return redirect('staff-profile')
        
    context = {'form': form, 'staff': staff}
    return render(request, 'users/staff/staff_update_profile.html', context)

@login_required(login_url='staff-login')
@allowed_users(allowed_roles=['staff'])
def staffDeleteProfile(request):
    staff = Staff.objects.get(user=request.user)

    if request.method == 'POST':
        staff.user.delete()
        return redirect('landing-page')
    
    context = {'staff': staff}
    return render(request, 'users/staff/staff_delete_profile.html', context)

@login_required(login_url='staff-login')
@allowed_users(allowed_roles=['staff'])
def staffDashboard(request):
    staff = Staff.objects.get(user=request.user)

    context = {'staff': staff}    
    return render(request, 'users/staff/staff_dashboard.html', context)
