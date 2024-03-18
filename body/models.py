# models.py
from django.db import models

class BodyPart(models.Model):
    name = models.CharField(max_length=100)
    note = models.TextField()
