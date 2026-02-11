from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('packages', '0002_package_extra_fields'),
        ('units', '0001_initial'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='package',
            name='status',
            field=models.CharField(choices=[('PENDING', 'Pendente'), ('DELIVERED', 'Entregue'), ('ARCHIVED', 'Arquivada'), ('CANCELLED', 'Cancelada')], default='PENDING', max_length=20),
        ),
        migrations.AddField(
            model_name='package',
            name='tracking_code',
            field=models.CharField(blank=True, max_length=80),
        ),
        migrations.CreateModel(
            name='PackageAuditLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('recipient_name', models.CharField(blank=True, max_length=255)),
                ('delivery_type', models.CharField(blank=True, max_length=20)),
                ('store', models.CharField(blank=True, max_length=80)),
                ('bank', models.CharField(blank=True, max_length=80)),
                ('tracking_code', models.CharField(blank=True, max_length=80)),
                ('received_at', models.DateTimeField(blank=True, null=True)),
                ('picked_up_at', models.DateTimeField(blank=True, null=True)),
                ('picked_up_by_name', models.CharField(max_length=255)),
                ('picked_up_by_document', models.CharField(blank=True, max_length=80)),
                ('picked_up_quantity', models.PositiveIntegerField(default=1)),
                ('notes', models.TextField(blank=True)),
                ('action', models.CharField(choices=[('PICKED_UP', 'Retirada'), ('RETURNED', 'Retornada'), ('CANCELLED', 'Cancelada')], default='PICKED_UP', max_length=20)),
                ('condominium', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='condominiums.condominium')),
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='audit_logs', to='packages.package')),
                ('picked_up_by_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='picked_package_logs', to='accounts.user')),
                ('received_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='received_package_logs', to='accounts.user')),
                ('unit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='units.unit')),
            ],
        ),
    ]
