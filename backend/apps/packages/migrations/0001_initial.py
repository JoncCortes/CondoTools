from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True
    dependencies = [('units', '0001_initial')]

    operations = [
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('description', models.CharField(max_length=255)),
                ('received_at', models.DateTimeField(auto_now_add=True)),
                ('delivered_at', models.DateTimeField(blank=True, null=True)),
                ('condominium', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='condominiums.condominium')),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='packages', to='units.unit')),
            ],
        ),
    ]
