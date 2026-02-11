from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True
    dependencies = [('accounts', '0001_initial'), ('common_areas', '0001_initial'), ('units', '0001_initial')]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('start_at', models.DateTimeField()),
                ('end_at', models.DateTimeField()),
                ('status', models.CharField(default='REQUESTED', max_length=32)),
                ('condominium', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='condominiums.condominium')),
                ('common_area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='common_areas.commonarea')),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='units.unit')),
                ('resident', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.user')),
            ],
        ),
    ]
