from django.contrib import admin
from .models import Consultation, Medication, MedicationCategory, PhototherapySession, Prescription, TreatmentPlan

admin.site.register(Consultation)
admin.site.register(Medication)
admin.site.register(MedicationCategory)
admin.site.register(PhototherapySession)
admin.site.register(Prescription)
admin.site.register(TreatmentPlan)