# Generated by Django 5.0.2 on 2024-03-12 06:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('query', '0004_alter_query_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='query',
            name='follow_up_required',
        ),
        migrations.RemoveField(
            model_name='query',
            name='resolution_notes',
        ),
        migrations.RemoveField(
            model_name='query',
            name='resolution_time',
        ),
        migrations.CreateModel(
            name='Resolution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resolution_notes', models.TextField()),
                ('resolution_time', models.DateTimeField(auto_now_add=True)),
                ('query', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='query.query')),
            ],
        ),
    ]
