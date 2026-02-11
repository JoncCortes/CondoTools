from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True
    dependencies = [('accounts','0001_initial'),('condominiums','0001_initial')]

    operations = [
        migrations.CreateModel(
            name='AuditLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('action', models.CharField(choices=[('CREATE', 'CREATE'), ('UPDATE', 'UPDATE'), ('DELETE', 'DELETE')], max_length=10)),
                ('model', models.CharField(max_length=120)),
                ('object_id', models.CharField(max_length=64)),
                ('changes', models.JSONField(blank=True, default=dict)),
                ('condominium', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='condominiums.condominium')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.user')),
            ],
            options={'ordering': ['-created_at']},
        ),
    ]
