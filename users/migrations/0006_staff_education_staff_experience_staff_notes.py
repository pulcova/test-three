# Generated by Django 5.0.2 on 2024-03-06 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_staff_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='education',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='staff',
            name='experience',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='staff',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
    ]
