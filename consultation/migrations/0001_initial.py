# Generated by Django 4.2.11 on 2024-03-14 12:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0007_alter_staff_department_alter_staff_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='Consultation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('doctors_notes', models.TextField(blank=True)),
                ('staff_instructions', models.TextField(blank=True)),
                ('doctor', models.ForeignKey(limit_choices_to={'is_staff': True}, on_delete=django.db.models.deletion.PROTECT, to='users.doctor')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.patient')),
            ],
        ),
        migrations.CreateModel(
            name='Medication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('brand_name', models.CharField(max_length=255)),
                ('generic_name', models.CharField(max_length=255)),
                ('dosage_forms', models.CharField(max_length=255)),
                ('dosage_strength', models.CharField(max_length=255)),
                ('side_effects', models.TextField(blank=True)),
                ('cost', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='MedicationCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('notes', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Prescription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dosage_quantity', models.CharField(max_length=50)),
                ('dosage_unit', models.CharField(max_length=50)),
                ('frequency', models.CharField(max_length=255)),
                ('refills', models.PositiveIntegerField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('instructions', models.TextField(blank=True)),
                ('status', models.CharField(choices=[('ACTIVE', 'Active'), ('DISCONTINUED', 'Discontinued')], default='ACTIVE', max_length=20)),
                ('notes', models.TextField(blank=True)),
                ('consultation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='consultation.consultation')),
                ('medication', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='consultation.medication')),
            ],
        ),
        migrations.CreateModel(
            name='TreatmentPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.patient')),
                ('prescriptions', models.ManyToManyField(blank=True, to='consultation.prescription')),
            ],
        ),
        migrations.CreateModel(
            name='PhototherapySession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('dosage', models.CharField(max_length=50)),
                ('device_type', models.CharField(blank=True, max_length=100)),
                ('area_treated', models.CharField(blank=True, max_length=255)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.patient')),
                ('staff', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.staff')),
                ('treatment_plan', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='consultation.treatmentplan')),
            ],
        ),
        migrations.AddField(
            model_name='medication',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='consultation.medicationcategory'),
        ),
    ]
