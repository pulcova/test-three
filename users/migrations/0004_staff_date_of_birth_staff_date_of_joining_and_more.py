# Generated by Django 5.0.2 on 2024-03-06 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_doctor_education_alter_doctor_experience'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='staff',
            name='date_of_joining',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='staff',
            name='department',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='staff',
            name='emergency_contact_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='staff',
            name='emergency_contact_phone',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='staff',
            name='gender',
            field=models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=1, null=True),
        ),
    ]
