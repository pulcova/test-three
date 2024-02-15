from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Doctor, Patient, Staff

class CreateDoctorForm(ModelForm):
    class Meta:
        model = Doctor
        fields = '__all__'

class CreatePatientForm(ModelForm):
    class Meta:
        model = Patient
        fields = '__all__'

class CreateStaffForm(ModelForm):
    class Meta:
        model = Staff
        fields = '__all__'

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']