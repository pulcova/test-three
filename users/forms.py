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
        fields = ['name', 'email', 'phone', 'profile_picture', 'date_of_birth', 'gender', 'address', 'specialization', 'license_number', 'education', 'experience', 'notes']

class CreatePatientForm(ModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'email', 'phone']

class PatientUpdateForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'email', 'phone', 'profile_picture', 'date_of_birth', 'gender', 'address', 'blood_group', 'weight', 'height', 'allergies', 'medical_history', 'emergency_contact_name', 'emergency_contact_phone']

class CreateStaffForm(ModelForm):
    class Meta:
        model = Staff
        fields = ['name', 'email', 'phone']

class StaffUpdateForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['name', 'email', 'phone', 'profile_picture', 'role']

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

