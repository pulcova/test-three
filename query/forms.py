from django import forms

from .models import Query, Resolution
from users.models import Doctor

class PatientQueryRaiseForm(forms.ModelForm):
    class Meta:
        model = Query
        fields = ['text', 'category', 'priority', 'supporting_document', 'notes']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'supporting_document': forms.FileInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class ResolutionForm(forms.ModelForm):
    class Meta:
        model = Resolution
        fields = ['resolution_notes']

class AssignDoctorForm(forms.ModelForm):
    class Meta:
        model = Query
        fields = ['doctor']

class ChangePriorityForm(forms.ModelForm):
    class Meta:
        model = Query
        fields = ['priority']

class ChangeCategoryForm(forms.ModelForm):
    class Meta:
        model = Query
        fields = ['category']
