# Generated by Django 3.2.8 on 2022-03-15 16:50

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('capstone', '0004_remove_ticket_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='route',
            name='passenger',
            field=models.ManyToManyField(related_name='passenger', to=settings.AUTH_USER_MODEL),
        ),
    ]
