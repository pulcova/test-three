from django.contrib import admin
from .models import Appointment, AppointmentException

admin.site.register(Appointment)
admin.site.register(AppointmentException)
