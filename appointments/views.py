from django.shortcuts import render
from users.models import Doctor
from django.shortcuts import redirect
from users.decorators import allowed_users
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.http import HttpResponseBadRequest
from django.contrib.auth.decorators import login_required

from  users.models import Patient, Doctor
from .models import Appointment
from .forms import PatientAppointmentForm
from users.decorators import allowed_users

@login_required(login_url='patient-login')
@allowed_users(allowed_roles=['patient'])
def submit_appointment(request):
    patient = request.user.patient  

    doctor = get_object_or_404(Doctor)

    if request.method == 'POST':
        form = PatientAppointmentForm(request.POST)
        if form.is_valid():
            form.instance.patient = patient
            form.instance.doctor = doctor
            form.save()
            return redirect('appointment-success')
    else:
        form = PatientAppointmentForm(initial={'patient': patient, 'doctor': doctor})
    return render(request, 'appointments/patient_appointment_form.html', {'form': form})

@login_required(login_url='patient-login')
@allowed_users(allowed_roles=['patient'])
def appointment_success(request):
    return render(request, 'appointments/patient_appointment_success.html')

@login_required(login_url='patient-login')
@allowed_users(allowed_roles=['patient'])
def patient_calendar_view(request):
    user = request.user
    
    patient = get_object_or_404(Patient, user=user)
    
    patient_appointments = Appointment.objects.filter(patient=patient, date_and_time__isnull=False)
    
    serialized_appointments = [{
        'title': appointment.reason,  
        'start': appointment.date_and_time.isoformat() if appointment.date_and_time else None,
    } for appointment in patient_appointments]
    
    return render(request, 'appointments/patient_calendar.html', {'appointments': serialized_appointments})


@login_required(login_url='doctor-login')
@allowed_users(allowed_roles=['doctor'])
def doctor_calendar_view(request):
    return render(request, 'appointments/doctor_calendar.html')

@login_required(login_url='staff-login')
@allowed_users(allowed_roles=['staff'])
def staff_calendar_view(request):
    return render(request, 'appointments/staff_calendar.html')


@login_required(login_url='patient-login')
@allowed_users(allowed_roles=['patient'])
def view_patient_appointments(request):
    patient = request.user.patient 
    appointments = Appointment.objects.filter(patient=patient).order_by('-date_and_time')

    context = {
        'appointments': appointments
    }
    return render(request, 'appointments/patient_appointment_list.html', context)