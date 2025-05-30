# Generated by Django 5.2.1 on 2025-05-07 21:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('companies', '0001_initial'),
        ('passengers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plate_number', models.CharField(max_length=20, unique=True)),
                ('vehicle_type', models.CharField(max_length=50)),
                ('capacity', models.PositiveIntegerField()),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vehicles', to='companies.company')),
            ],
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departure_time', models.DateTimeField()),
                ('destination', models.CharField(max_length=100)),
                ('fee_per_passenger', models.DecimalField(decimal_places=2, default=500.0, max_digits=10)),
                ('is_completed', models.BooleanField(default=False)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trips', to='companies.company')),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trips', to='trips.vehicle')),
            ],
        ),
        migrations.CreateModel(
            name='TripPassenger',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seat_number', models.CharField(blank=True, max_length=10, null=True)),
                ('passenger', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trips', to='passengers.passenger')),
                ('trip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='passengers', to='trips.trip')),
            ],
            options={
                'unique_together': {('trip', 'passenger')},
            },
        ),
    ]
