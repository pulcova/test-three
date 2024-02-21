from django.shortcuts import render, redirect
from .forms import PatientPrescriptionForm, PatientReportForm, PatientBillsForm, PatientVaccinationForm
from django.contrib.auth.decorators import login_required

def docs_dashboard(request):
    return render(request, 'docs/docs_dashboard.html')

def select_upload_category(request):
    return render(request, 'docs/select_upload_category.html')


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


def upload_report(request):
    if request.method == 'POST':
        form = PatientReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.patient = request.user.patient
            report.save()
            return redirect('select_upload_category')
    else:
        form = PatientReportForm()
    return render(request, 'docs/upload_report.html', {'form': form})


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
