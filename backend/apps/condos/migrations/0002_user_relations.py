from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0001_initial'),
        ('condos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='resident',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.user'),
        ),
        migrations.AddField(
            model_name='staff',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.user'),
        ),
        migrations.AddField(
            model_name='package',
            name='received_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.user'),
        ),
        migrations.AddField(
            model_name='incident',
            name='reporter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.user'),
        ),
        migrations.AddField(
            model_name='reservation',
            name='resident',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.user'),
        ),
    ]
