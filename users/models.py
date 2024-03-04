from django.db import models
from django.contrib.auth.models import User
from django.templatetags.static import static

class Doctor(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    date_of_birth = models.DateField(null=True, blank=True)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    specialization = models.CharField(max_length=100, null=True, blank=True)
    license_number = models.CharField(max_length=100, null=True, blank=True)
    education = models.TextField(null=True, blank=True)
    experience = models.TextField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    profile_picture = models.ImageField(null=True, blank=True, upload_to='profile_pictures/doctor/')

    def save(self, *args, **kwargs):
        if not self.profile_picture:
            self.profile_picture = static('images/profile.png')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Patient(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    date_of_birth = models.DateField(null=True, blank=True)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    blood_group = models.CharField(max_length=10, null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    allergies = models.TextField(null=True, blank=True)
    medical_history = models.TextField(null=True, blank=True)
    emergency_contact_name = models.CharField(max_length=100, null=True, blank=True)
    emergency_contact_phone = models.CharField(max_length=15, null=True, blank=True)
    profile_picture = models.ImageField(null=True, blank=True, upload_to='profile_pictures/patient/')

    def save(self, *args, **kwargs):
        if not self.profile_picture:
            self.profile_picture = static('images/profile.png')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class Staff(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    role = models.CharField(max_length=100, null=True, blank=True)
    profile_picture = models.ImageField(null=True, blank=True, upload_to='profile_pictures/staff/')

    def save(self, *args, **kwargs):
        if not self.profile_picture:
            self.profile_picture = static('images/profile.png')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name