from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('residents', '0001_initial'),
        ('packages', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='package',
            name='bank',
            field=models.CharField(blank=True, max_length=80),
        ),
        migrations.AddField(
            model_name='package',
            name='delivery_type',
            field=models.CharField(choices=[('LETTER', 'Carta registrada'), ('PACKAGE', 'Encomenda')], default='PACKAGE', max_length=20),
        ),
        migrations.AddField(
            model_name='package',
            name='other_bank',
            field=models.CharField(blank=True, max_length=120),
        ),
        migrations.AddField(
            model_name='package',
            name='other_store',
            field=models.CharField(blank=True, max_length=120),
        ),
        migrations.AddField(
            model_name='package',
            name='resident',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='packages', to='residents.resident'),
        ),
        migrations.AddField(
            model_name='package',
            name='store',
            field=models.CharField(blank=True, max_length=80),
        ),
    ]
