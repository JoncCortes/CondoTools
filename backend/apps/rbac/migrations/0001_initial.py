from django.db import migrations, models
import django.db.models.deletion


def seed_role_permissions(apps, schema_editor):
    RolePermissionSet = apps.get_model('rbac', 'RolePermissionSet')
    from apps.rbac.registry import ROLE_DEFAULTS

    for role, perms in ROLE_DEFAULTS.items():
        RolePermissionSet.objects.get_or_create(
            role=role,
            condominium=None,
            defaults={"permissions": perms},
        )


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        ('condominiums', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RolePermissionSet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('PLATFORM_ADMIN', 'Platform Admin'), ('SINDICO', 'Síndico'), ('PORTEIRO', 'Porteiro'), ('MORADOR', 'Morador')], max_length=20)),
                ('permissions', models.JSONField(blank=True, default=list)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('condominium', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='condominiums.condominium')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_role_permissions', to='accounts.user')),
            ],
            options={'ordering': ['role', 'id']},
        ),
        migrations.AlterUniqueTogether(name='rolepermissionset', unique_together={('role', 'condominium')}),
        migrations.RunPython(seed_role_permissions, migrations.RunPython.noop),
    ]
