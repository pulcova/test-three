# Generated by Django 5.0.2 on 2024-03-06 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_staff_date_of_birth_staff_date_of_joining_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='address',
            field=models.TextField(blank=True, null=True),
        ),
    ]