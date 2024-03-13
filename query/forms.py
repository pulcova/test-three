from django import forms

from .models import Query, Resolution, FollowUp
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
    doctor = forms.ModelChoiceField(
        queryset=Doctor.objects.all(),
        widget=forms.Select(attrs={'class': 'mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'})
    ) 

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

class QueryUpdateForm(forms.ModelForm):
    class Meta:
        model = Query
        fields = ['status', 'priority', 'doctor']  



class UpdatePriorityForm(forms.ModelForm):
    class Meta:
        model = Query
        fields = ['priority']

class UpdateStatusForm(forms.ModelForm):
    class Meta:
        model = Query
        fields = ['status']

class FollowUpForm(forms.ModelForm):
    class Meta:
        model = FollowUp
        fields = ['notes']


