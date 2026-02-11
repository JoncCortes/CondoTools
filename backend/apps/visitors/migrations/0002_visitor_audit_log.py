from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('visitors', '0001_initial'),
        ('units', '0001_initial'),
    ]

    operations = [
        migrations.AddField(model_name='visitor', name='authorized_by', field=models.CharField(blank=True, max_length=255)),
        migrations.AddField(model_name='visitor', name='is_active', field=models.BooleanField(default=True)),
        migrations.AddField(model_name='visitor', name='notes', field=models.TextField(blank=True)),
        migrations.CreateModel(
            name='VisitorAuditLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('visitor_name', models.CharField(max_length=255)),
                ('document', models.CharField(blank=True, max_length=32)),
                ('authorized_by', models.CharField(blank=True, max_length=255)),
                ('entry_at', models.DateTimeField(blank=True, null=True)),
                ('exit_at', models.DateTimeField(blank=True, null=True)),
                ('notes', models.TextField(blank=True)),
                ('status', models.CharField(choices=[('INSIDE', 'Inside'), ('EXITED', 'Exited'), ('DENIED', 'Denied')], default='INSIDE', max_length=12)),
                ('condominium', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='condominiums.condominium')),
                ('finalized_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='visitor_finalized_logs', to='accounts.user')),
                ('registered_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='visitor_registered_logs', to='accounts.user')),
                ('unit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='units.unit')),
                ('visitor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='audit_logs', to='visitors.visitor')),
            ],
        ),
    ]
