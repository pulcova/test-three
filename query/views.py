from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from users.decorators import allowed_users
from django.contrib import messages

from .forms import PatientQueryRaiseForm, AssignDoctorForm, ResolutionForm, ChangePriorityForm, ChangeCategoryForm
from .models import Query, Resolution
from users.models import Staff, Patient, Doctor
from organization.models import Role


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
    'APPT': ['IT Support', 'Licensed Practical Nurse (LPN)', 'Physician Assistant (PA)', 'Office Manager', 'Registered Nurse (RN)', 'Receptionist'], 
    'OTHER': ['Facilities/Maintenance', 'IT Support', 'Nutritionist/Dietitian', 'Mental Health Counseling', 'Occupational Therapy', 'Physical Therapy', 'Medical Records Clerk'],
    'MED': ['Nurse Practitioner (NP)', 'Physician Assistant (PA)', 'Licensed Practical Nurse (LPN)', 'Registered Nurse (RN)', 'Medical Technician/Technologist', 'Phlebotomist', 'Medical Assistant (MA)'],
    'BILL': ['Billing Specialist'],
    }

    if request.method == 'POST':
        form = PatientQueryRaiseForm(request.POST, request.FILES)
        if form.is_valid():
            query = form.save(commit=False)  
            query.patient = patient
            query.save()  

            if query.category in CATEGORY_TO_ROLE_MAPPING:
                roles_for_category = CATEGORY_TO_ROLE_MAPPING[query.category] 
                potential_staff = Staff.objects.filter(role__name__in=roles_for_category)

                staff_to_assign = potential_staff[:2]  
                query.assigned_staff.add(*staff_to_assign)

            return redirect('patient-queries-list')
    else:
        form = PatientQueryRaiseForm()

    context = {
        'form': form,
    }
    return render(request, 'query/patient_raise_query.html', context)



def queris_inbox_staff(request):
    staff_member = get_object_or_404(Staff, user=request.user) 
    queries = Query.objects.filter(assigned_staff=staff_member) 

    return render(request, 'query/staff_queries_inbox.html', {'queries': queries})


def query_detail_staff(request, query_id):
    query = get_object_or_404(Query, pk=query_id)
    return render(request, 'query/staff_query_detail.html', {'query': query})

def staff_query_detail(request, query_id):
    query = get_object_or_404(Query, pk=query_id)
    resolution = query.resolution if hasattr(query, 'resolution') else None
    resolution_form = ResolutionForm(instance=resolution) if resolution else None
    assign_doctor_form = AssignDoctorForm(initial={'doctor': query.doctor_id})
    change_priority_form = ChangePriorityForm(initial={'priority': query.priority})
    change_category_form = ChangeCategoryForm(initial={'category': query.category})

    if request.method == 'POST':
        if 'resolution_notes' in request.POST:
            resolution_form = ResolutionForm(request.POST, instance=resolution)
            if resolution_form.is_valid():
                resolution = resolution_form.save(commit=False)
                resolution.query = query
                resolution.save()
        elif 'doctor' in request.POST:
            assign_doctor_form = AssignDoctorForm(request.POST)
            if assign_doctor_form.is_valid():
                query.doctor = assign_doctor_form.cleaned_data['doctor']
                query.save()
        elif 'priority' in request.POST:
            change_priority_form = ChangePriorityForm(request.POST)
            if change_priority_form.is_valid():
                query.priority = change_priority_form.cleaned_data['priority']
                query.save()
        elif 'category' in request.POST:
            change_category_form = ChangeCategoryForm(request.POST)
            if change_category_form.is_valid():
                query.category = change_category_form.cleaned_data['category']
                query.save()

        return redirect('staff-query-detail', query_id=query_id)

    context = {
        'query': query,
        'resolution': resolution,
        'resolution_form': resolution_form,
        'assign_doctor_form': assign_doctor_form,
        'change_priority_form': change_priority_form,
        'change_category_form': change_category_form,
    }
    return render(request, 'query/staff_query_detail.html', context)