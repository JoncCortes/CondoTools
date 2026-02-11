from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        ('condominiums', '0001_initial'),
        ('units', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceProvider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('provider_name', models.CharField(max_length=255)),
                ('company', models.CharField(blank=True, max_length=255)),
                ('document', models.CharField(blank=True, max_length=80)),
                ('service_type', models.CharField(max_length=120)),
                ('authorized_by', models.CharField(blank=True, max_length=255)),
                ('notes', models.TextField(blank=True)),
                ('status', models.CharField(default='ACTIVE', max_length=12)),
                ('condominium', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='condominiums.condominium')),
                ('unit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='units.unit')),
            ],
        ),
        migrations.CreateModel(
            name='ServiceProviderAuditLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('provider_name', models.CharField(max_length=255)),
                ('company', models.CharField(blank=True, max_length=255)),
                ('document', models.CharField(blank=True, max_length=80)),
                ('service_type', models.CharField(max_length=120)),
                ('entry_at', models.DateTimeField(blank=True, null=True)),
                ('exit_at', models.DateTimeField(blank=True, null=True)),
                ('authorized_by', models.CharField(blank=True, max_length=255)),
                ('notes', models.TextField(blank=True)),
                ('status', models.CharField(choices=[('ACTIVE', 'Active'), ('FINISHED', 'Finished'), ('DENIED', 'Denied')], default='ACTIVE', max_length=12)),
                ('condominium', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='condominiums.condominium')),
                ('finalized_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='provider_finalized_logs', to='accounts.user')),
                ('registered_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='provider_registered_logs', to='accounts.user')),
                ('service_provider', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='audit_logs', to='service_providers.serviceprovider')),
                ('unit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='units.unit')),
            ],
        ),
    ]
