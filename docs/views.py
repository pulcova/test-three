from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.http import FileResponse, Http404

from .forms import PatientPrescriptionForm, PatientReportForm, PatientBillsForm, PatientVaccinationForm
from .models import PatientPrescription, PatientReport, PatientBills, PatientVaccination
from users.models import Patient
from users.decorators import allowed_users

import os

@login_required(login_url='patient-login')
@allowed_users(allowed_roles=['patient'])
def docs_dashboard(request):
    user = request.user
    patient = get_object_or_404(Patient, user=user)

    patient_bills = PatientBills.objects.filter(patient=patient)
    patient_prescriptions = PatientPrescription.objects.filter(patient=patient)
    patient_reports = PatientReport.objects.filter(patient=patient)
    patient_vaccinations = PatientVaccination.objects.filter(patient=patient)
    
    context = {
        'patient': patient,
        'patient_bills': patient_bills,
        'patient_prescriptions': patient_prescriptions,
        'patient_reports': patient_reports,
        'patient_vaccinations': patient_vaccinations,
    }
    return render(request, 'docs/docs_dashboard.html', context)

@login_required(login_url='patient-login')
@allowed_users(allowed_roles=['patient'])
def select_upload_category(request):
    return render(request, 'docs/select_upload_category.html')

@login_required(login_url='patient-login')
@allowed_users(allowed_roles=['patient'])
def upload_prescription(request):
    if request.method == 'POST':
        form = PatientPrescriptionForm(request.POST, request.FILES)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.patient = request.user.patient 
            prescription.save()
            return redirect('select_upload_category')
    else:
        form = PatientPrescriptionForm()
    return render(request, 'docs/upload_prescription.html', {'form': form})

@login_required(login_url='patient-login')
@allowed_users(allowed_roles=['patient'])
def upload_report(request):
    if request.method == 'POST':
        form = PatientReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.patient = request.user.patient
            report.save()
            print(report.report.url)
            return redirect('select_upload_category')
    else:
        form = PatientReportForm()
    return render(request, 'docs/upload_report.html', {'form': form})

@login_required(login_url='patient-login')
@allowed_users(allowed_roles=['patient'])
def upload_bill(request):
    if request.method == 'POST':
        form = PatientBillsForm(request.POST, request.FILES)
        if form.is_valid():
            bill = form.save(commit=False)
            bill.patient = request.user.patient
            bill.save()
            return redirect('select_upload_category')
    else:
        form = PatientBillsForm()
    return render(request, 'docs/upload_bill.html', {'form': form})

@login_required(login_url='patient-login')
@allowed_users(allowed_roles=['patient'])
def upload_vaccination(request):
    if request.method == 'POST':
        form = PatientVaccinationForm(request.POST, request.FILES)
        if form.is_valid():
            vaccination = form.save(commit=False)
            vaccination.patient = request.user.patient
            vaccination.save()
            return redirect('select_upload_category')
    else:
        form = PatientVaccinationForm()
    return render(request, 'docs/upload_vaccination.html', {'form': form})

def view_prescription(request, prescription_id):
    print(prescription_id)
    prescription = get_object_or_404(PatientPrescription, pk=prescription_id)

    response = FileResponse(prescription.prescription.file)
    return response

def view_bill(request, bill_id):
    print(bill_id)
    prescription = get_object_or_404(PatientPrescription, pk=bill_id)

    response = FileResponse(prescription.prescription.file)
    return response

def view_report(request, report_id):
    print(report_id)
    report = get_object_or_404(PatientReport, pk=report_id)

    response = FileResponse(report.report.file)
    return response

def view_vaccination(request, vaccination_id):
    print(vaccination_id)
    vaccination = get_object_or_404(PatientVaccination, pk=vaccination_id)

    response = FileResponse(vaccination.vaccine.file)
    return response