# Generated by Django 5.0.2 on 2024-02-28 05:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0002_alter_appointment_status'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Slot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.TimeField(blank=True, null=True)),
                ('end_time', models.TimeField(blank=True, null=True)),
                ('date', models.DateField(blank=True, null=True)),
                ('is_available', models.BooleanField(default=True)),
                ('doctor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.doctor')),
            ],
        ),
    ]
