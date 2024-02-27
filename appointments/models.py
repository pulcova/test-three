from django.db import models
from users.models import Doctor, Patient, Staff
from datetime import timedelta, date
from django.core.mail import send_mail

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
    date_and_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, blank=True, default='scheduled')
    mode = models.CharField(max_length=10, choices=MODE_CHOICES, default='in-person')
    color_code = models.CharField(max_length=1, choices=COLOR_CHOICES, default='A')
    reason = models.TextField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    details_confirmation = models.BooleanField(default=False)

    def schedule_follow_up_reminder(self):
        reminder_date = self.date_and_time - timedelta(days=45)
        if reminder_date > date.today():
            patient_email = self.patient.email
            subject = "Follow-up Appointment Reminder"
            message = f"Dear {self.patient.name},\n\nThis is a reminder for your follow-up appointment scheduled on {self.date_and_time.date()}. Please ensure you are available.\n\nRegards,\nThe Clinic"
            send_mail(subject, message, 'clinic@example.com', [patient_email])

    def schedule_block_appointment(self):
        block_date = self.date_and_time + timedelta(days=30)
        if block_date > date.today():
            staff_emails = [staff.email for staff in Staff.objects.all()]  
            subject = "Blocked Appointment Notification"
            message = f"Dear Team,\n\nThis is to inform you that the appointment scheduled on {self.date_and_time.date()} has been blocked. Please take necessary actions.\n\nRegards,\nThe Clinic"
            send_mail(subject, message, 'clinic@example.com', staff_emails)

class AppointmentException(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    authorized_by = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True)  
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
