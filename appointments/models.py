from django.db import models
from users.models import Doctor, Patient, Staff
from datetime import timedelta, date
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime, timedelta

class Appointment(models.Model):
    STATUS_CHOICES = (
        ('scheduled', 'Scheduled'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
        ('rescheduled', 'Rescheduled'),
    )
    COLOR_CHOICES = (
        ('A', 'Red'),
        ('B', 'Green'),
        ('C', 'Blue'),
    )
    MODE_CHOICES = (
        ('in-person', 'In-Person'),
        ('telehealth', 'Telehealth'),
    )
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    date_and_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, blank=True, default='scheduled')
    mode = models.CharField(max_length=10, choices=MODE_CHOICES, default='in-person')
    color_code = models.CharField(max_length=1, choices=COLOR_CHOICES, default='A')
    reason = models.TextField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    details_confirmation = models.BooleanField(default=False)
    supporting_document = models.FileField(upload_to='patient_appointment_documents/', null=True, blank=True)

    def schedule_follow_up(self):
        if self.date is None or self.start_time is None:
            raise ValueError("date and start_time cannot be None")
        date_and_time = datetime.combine(self.date, self.start_time)
        follow_up_due_date = date_and_time - timedelta(days=45)
        follow_up = FollowUp.objects.create(appointment=self, due_date=follow_up_due_date)
        return follow_up

    def schedule_block_appointment(self):
        if self.date is None or self.start_time is None:
            raise ValueError("date and start_time cannot be None")
        date_and_time = datetime.combine(self.date, self.start_time)
        block_date = date_and_time + timedelta(days=30)
        if block_date.date() > date.today():
            staff_emails = [staff.email for staff in Staff.objects.all()]  
            subject = "Blocked Appointment Notification"
            message = f"Dear Team,\n\nThis is to inform you that the appointment scheduled on {date_and_time.date()} has been blocked. Please take necessary actions.\n\nRegards,\nThe Clinic"
            send_mail(subject, message, settings.EMAIL_HOST_USER, staff_emails)

    def __str__(self):
        return f"Appointment for {self.patient} with {self.doctor} on {self.date} at {self.start_time}"

class AppointmentException(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    authorized_by = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True)  
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Exception for appointment: {self.appointment}"

class FollowUp(models.Model):
    appointment = models.ForeignKey(Appointment, null=True, on_delete=models.CASCADE)
    due_date = models.DateField(blank=True, null=True)
    notification_sent = models.BooleanField(default=False)

    def __str__(self):
        return f"Follow-up for appointment: {self.appointment}"

class Slot(models.Model):
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    doctor = models.ForeignKey(Doctor, null=True, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"Slot for {self.doctor} on {self.date} from {self.start_time} to {self.end_time}"
