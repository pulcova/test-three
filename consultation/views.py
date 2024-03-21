from django.shortcuts import render
from django.shortcuts import get_object_or_404

from .models import Consultation

def consultation_overview(request):
    consultation = get_object_or_404(Consultation)
    context = {'consultation': consultation}
    return render(request, 'consultation/consultation_overview.html', context)