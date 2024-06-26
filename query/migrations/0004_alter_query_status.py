# Generated by Django 5.0.2 on 2024-03-12 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('query', '0003_query_supporting_document'),
    ]

    operations = [
        migrations.AlterField(
            model_name='query',
            name='status',
            field=models.CharField(choices=[('OPEN', 'Open'), ('PROG', 'In-Progress'), ('RES', 'Resolved'), ('CLOSED', 'Closed')], default='OPEN', max_length=10),
        ),
    ]
