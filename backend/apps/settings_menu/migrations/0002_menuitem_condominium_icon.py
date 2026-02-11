from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("condominiums", "0001_initial"),
        ("settings_menu", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="menuitem",
            name="condominium",
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name="menu_items", to="condominiums.condominium"),
        ),
        migrations.AddField(
            model_name="menuitem",
            name="icon",
            field=models.CharField(blank=True, max_length=80),
        ),
    ]
