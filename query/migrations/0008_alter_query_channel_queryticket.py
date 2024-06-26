# Generated by Django 5.0.2 on 2024-03-13 10:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('query', '0007_querycategory_notes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='query',
            name='channel',
            field=models.CharField(choices=[('WEB', 'Website'), ('CHAT', 'Chatbot'), ('SOCIAL', 'Social Media'), ('CALL', 'Direct Call'), ('IVR', 'IVR')], default='WEB', max_length=10),
        ),
        migrations.CreateModel(
            name='QueryTicket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticket_number', models.CharField(max_length=20, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('query', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='query.query')),
            ],
        ),
    ]
