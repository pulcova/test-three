from django.contrib import admin
from .models import PatientPrescription, PatientReport, PatientBills, PatientVaccination

admin.site.register(PatientPrescription)
admin.site.register(PatientReport)
admin.site.register(PatientBills)
admin.site.register(PatientVaccination)