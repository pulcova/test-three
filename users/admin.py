from django.contrib import admin
from .models import Doctor, Patient, Staff

admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Staff)