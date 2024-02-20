from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Doctor, Patient, Staff

class CreateDoctorForm(ModelForm):
    class Meta:
        model = Doctor
        fields = ['name', 'email', 'phone']

class DoctorUpdateForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['name', 'email', 'phone', 'profile_picture']

class CreatePatientForm(ModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'email', 'phone']

class PatientUpdateForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'email', 'phone', 'profile_picture']

class CreateStaffForm(ModelForm):
    class Meta:
        model = Staff
        fields = ['name', 'email', 'phone']

class StaffUpdateForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'email', 'phone', 'profile_picture']

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

