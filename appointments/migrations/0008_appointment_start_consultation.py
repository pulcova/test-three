# Generated by Django 4.2.11 on 2024-03-18 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0007_followup'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='start_consultation',
            field=models.BooleanField(default=False),
        ),
    ]
