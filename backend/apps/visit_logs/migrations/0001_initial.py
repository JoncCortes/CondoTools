from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('condominiums', '0001_initial'),
        ('visitors', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='VisitLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('entry_at', models.DateTimeField()),
                ('exit_at', models.DateTimeField(blank=True, null=True)),
                ('notes', models.TextField(blank=True)),
                ('condominium', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='condominiums.condominium')),
                ('visitor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='visit_logs', to='visitors.visitor')),
            ],
        ),
    ]
