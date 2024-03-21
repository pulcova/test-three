from django.shortcuts import render, redirect
from .models import BodyPart

def submit_body_part(request):
    if request.method == 'POST':
        coordinates = request.POST.get('coordinates') 
        name = request.POST.get('name')
        note = request.POST.get('note')

        # Process coordinates (if needed)
        x, y = map(int, coordinates.split(','))

        # Create BodyPart object
        body_part = BodyPart(name=name, note=note) 
        body_part.save()

        return redirect('appointment-booking-form')  # Redirect to success page
    else:
        return render(request, 'appointments/appointment_booking_form.html')



def display_3d_model(request):
    model_name = 'male.glb'  
    context = {'model_name': model_name}
    return render(request, 'body/model_viewer_template.html', context)
