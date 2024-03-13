from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from django.utils.decorators import method_decorator
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.core.mail import send_mail

from .models import Query
from users.decorators import allowed_users
from .forms import ResolutionForm, PatientQueryRaiseForm, AssignDoctorForm, QueryUpdateForm, UpdatePriorityForm, UpdateStatusForm
from .models import Query, Resolution
from users.models import Staff, Patient, Doctor
from .models import QueryTicket


@login_required(login_url='patient-login')
@allowed_users(allowed_roles=['patient'])
def patient_queries_list(request):
    user = request.user
    patient = get_object_or_404(Patient, user=user)
    patient_queries = Query.objects.filter(patient=patient)

    context = {
        'patient': patient,
        'patient_queries': patient_queries,
    }
    return render(request, 'query/patient_queries_list.html', context)


@login_required(login_url='patient-login')
@allowed_users(allowed_roles=['patient'])
def patient_query_detail(request, query_id):
    query = get_object_or_404(Query, pk=query_id, patient=request.user.patient)

    context = {
        'query': query,
        'resolutions': query.resolution_set.all(), 
    }
    return render(request, 'query/patient_query_detail.html', context)


@login_required(login_url='patient-login')
@allowed_users(allowed_roles=['patient'])
def patient_delete_query(request, query_id):
    query = get_object_or_404(Query, pk=query_id, patient=request.user.patient)  

    if request.method == 'POST':
        query.delete()

        return redirect('patient-queries-list')
    return render(request, 'query/patient_query_delete.html', {'query': query})


@login_required(login_url='patient-login')
@allowed_users(allowed_roles=['patient'])
def patient_raise_query(request):
    user = request.user
    patient = get_object_or_404(Patient, user=user)

    CATEGORY_TO_ROLE_MAPPING = {
        'Appointment': ['IT Support', 'Licensed Practical Nurse (LPN)', 'Physician Assistant (PA)', 'Office Manager', 'Registered Nurse (RN)', 'Receptionist'],  
        'Other': ['Facilities/Maintenance', 'IT Support', 'Nutritionist/Dietitian', 'Mental Health Counseling', 'Occupational Therapy', 'Physical Therapy', 'Medical Records Clerk'],
        'Medical': ['Nurse Practitioner (NP)', 'Physician Assistant (PA)', 'Licensed Practical Nurse (LPN)', 'Registered Nurse (RN)', 'Medical Technician/Technologist', 'Phlebotomist', 'Medical Assistant (MA)'],
        'Billing & Insurance': ['Billing Specialist'],
        'Feedback & Complaints': []  
    }

    if request.method == 'POST':
        form = PatientQueryRaiseForm(request.POST, request.FILES)
        if form.is_valid():
            query = form.save(commit=False)
            query.patient = patient
            query.save()  

            if query.category.name in CATEGORY_TO_ROLE_MAPPING:  
                roles_for_category = CATEGORY_TO_ROLE_MAPPING[query.category.name]
                potential_staff = Staff.objects.filter(role__name__in=roles_for_category)
                staff_to_assign = potential_staff[:2]
                query.assigned_staff.add(*staff_to_assign)

            return redirect('patient-queries-list')
    
    form = PatientQueryRaiseForm()
    return render(request, 'query/patient_raise_query.html', {'form': form})


@method_decorator([login_required(login_url='patient-login'), allowed_users(allowed_roles=['patient'])], name='dispatch')
class PatientQueryUpdateView(UpdateView):
    model = Query
    form_class = PatientQueryRaiseForm
    template_name = 'query/patient_query_update.html'

    def get_success_url(self):
        return reverse_lazy('patient-queries-list')

    def form_valid(self, form):
        query = form.save(commit=False)
        if self.request.user.patient != query.patient:
            return HttpResponseForbidden()
        return super().form_valid(form)


def queris_inbox_staff(request):
    staff_member = get_object_or_404(Staff, user=request.user) 
    queries = Query.objects.filter(assigned_staff=staff_member) 

    return render(request, 'query/staff_queries_inbox.html', {'queries': queries})


def staff_query_view(request, query_id):
    query = get_object_or_404(Query, pk=query_id)

    if request.user.staff not in query.assigned_staff.all(): 
        messages.error(request, "You are not authorized to view this query.")
        return redirect('some-other-view') 

    update_form = QueryUpdateForm(instance=query) 
    resolution_form = ResolutionForm()
    update_priority_form = UpdatePriorityForm(instance=query)
    update_status_form = UpdateStatusForm(instance=query)
    assign_doctor_form = AssignDoctorForm(instance=query)

    if request.method == 'POST':
        if 'update_priority' in request.POST:
            update_priority_form = UpdatePriorityForm(request.POST, instance=query)
            if update_priority_form.is_valid():
                update_priority_form.save()
                messages.success(request, 'Priority updated!')
                return redirect('staff-query-detail', query_id=query_id)
        elif 'update_status' in request.POST:
            update_status_form = UpdateStatusForm(request.POST, instance=query)
            if update_status_form.is_valid():
                update_status_form.save()
                messages.success(request, 'Status updated!')
                return redirect('staff-query-detail', query_id=query_id) 
        elif 'assign_doctor' in request.POST:
            assign_doctor_form = AssignDoctorForm(request.POST, instance=query)
            if assign_doctor_form.is_valid():
                assign_doctor_form.save()
                messages.success(request, 'Doctor assigned!')
                return redirect('staff-query-detail', query_id=query_id)
        elif 'add_resolution' in request.POST:  
            resolution_form = ResolutionForm(request.POST)
            if resolution_form.is_valid():
                new_resolution = Resolution.objects.create(
                    query=query,
                    user=request.user,
                    **resolution_form.cleaned_data
                )
                new_resolution.save()
                messages.success(request, 'Resolution added!')
                return redirect('staff-query-detail', query_id=query_id) 

    context = {
        'query': query, 
        'update_form': update_form,
        'update_priority_form': update_priority_form, 
        'update_status_form': update_status_form, 
        'assign_doctor_form': assign_doctor_form,
        'resolution_form': resolution_form, 
        'resolutions': query.resolution_set.all(),  
    }
    return render(request, 'query/staff_query_detail.html', context) 


def queries_inbox_doctor(request):
    doctor_member = get_object_or_404(Doctor, user=request.user) 
    queries = Query.objects.filter(doctor=doctor_member) 

    return render(request, 'query/doctor_queries_inbox.html', {'queries': queries})


def doctor_query_view(request, query_id):
    query = get_object_or_404(Query, pk=query_id)

    print(request.user.doctor, query.doctor)

    if request.user.doctor != query.doctor: 
        messages.error(request, "You are not authorized to view this query.")
        return redirect('some-other-view') 

    update_form = QueryUpdateForm(instance=query) 
    resolution_form = ResolutionForm()
    update_priority_form = UpdatePriorityForm(instance=query)
    update_status_form = UpdateStatusForm(instance=query)

    if request.method == 'POST':
        if 'update_priority' in request.POST:
            update_priority_form = UpdatePriorityForm(request.POST, instance=query)
            if update_priority_form.is_valid():
                update_priority_form.save()
                messages.success(request, 'Priority updated!')
                return redirect('doctor-query-detail', query_id=query_id)
        elif 'update_status' in request.POST:
            update_status_form = UpdateStatusForm(request.POST, instance=query)
            if update_status_form.is_valid():
                update_status_form.save()
                messages.success(request, 'Status updated!')
                return redirect('doctor-query-detail', query_id=query_id) 
        elif 'add_resolution' in request.POST:  
            resolution_form = ResolutionForm(request.POST)
            if resolution_form.is_valid():
                new_resolution = Resolution.objects.create(
                    query=query,
                    user=request.user,
                    **resolution_form.cleaned_data
                )
                new_resolution.save()
                messages.success(request, 'Resolution added!')
                return redirect('doctor-query-detail', query_id=query_id) 

    context = {
        'query': query, 
        'update_form': update_form,
        'update_priority_form': update_priority_form, 
        'update_status_form': update_status_form, 
        'resolution_form': resolution_form, 
        'resolutions': query.resolution_set.all(),  
    }
    return render(request, 'query/doctor_query_detail.html', context) 



