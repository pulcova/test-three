from django import forms
from .models import Appointment, AppointmentException

class PatientAppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['patient', 'doctor', 'start_time', 'end_time', 'date', 'mode', 'reason', 'notes', 'details_confirmation']

class AppointmentExceptionForm(forms.ModelForm):
    class Meta:
        model = AppointmentException
        fields = ['reason']

class DoctorAppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['patient', 'date_and_time', 'reason', 'notes', 'mode', 'details_confirmation']