from django import forms
from .models import PatientPrescription, PatientReport, PatientBills, PatientVaccination

class PatientPrescriptionForm(forms.ModelForm):
    class Meta:
        model = PatientPrescription
        fields = ['prescription']

class PatientReportForm(forms.ModelForm):
    class Meta:
        model = PatientReport
        fields = ['report']

class PatientBillsForm(forms.ModelForm):
    class Meta:
        model = PatientBills
        fields = ['bill']

class PatientVaccinationForm(forms.ModelForm):
    class Meta:
        model = PatientVaccination
        fields = ['vaccine']
