# Generated by Django 3.2.8 on 2022-03-15 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('capstone', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='ticketsNum',
            field=models.PositiveSmallIntegerField(blank=True, default=1, null=True),
        ),
    ]
