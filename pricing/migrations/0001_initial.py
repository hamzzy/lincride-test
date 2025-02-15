# Generated by Django 5.1.6 on 2025-02-13 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PricingParameters',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('base_fare', models.FloatField(default=2.5, help_text='Fixed starting price.')),
                ('per_km_rate', models.FloatField(default=1.0, help_text='Variable rate based on distance (per km).')),
                ('low_traffic_multiplier', models.FloatField(default=1.0, help_text='Multiplier for low traffic.')),
                ('normal_traffic_multiplier', models.FloatField(default=1.0, help_text='Multiplier for normal traffic.')),
                ('high_traffic_multiplier', models.FloatField(default=1.5, help_text='Multiplier for high traffic.')),
                ('peak_demand_multiplier', models.FloatField(default=1.8, help_text='Multiplier for peak demand.')),
                ('high_demand_multiplier', models.FloatField(default=1.2, help_text='Multiplier for high demand')),
                ('rush_hour_multiplier', models.FloatField(default=1.3, help_text='Multiplier during rush hours (7-9am and 5-7pm).')),
                ('max_surge_multiplier', models.FloatField(default=2.2, help_text='Maximum surge multiplier')),
            ],
            options={
                'verbose_name_plural': 'Pricing Parameters',
            },
        ),
    ]
