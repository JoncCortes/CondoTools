from django.db import migrations, models


def populate_number_from_code(apps, schema_editor):
    Unit = apps.get_model("units", "Unit")
    for unit in Unit.objects.all():
        if unit.number:
            continue
        raw = (unit.code or "").strip()
        number = raw.split("-")[-1] if raw else f"{unit.id}"
        unit.number = number
        unit.save(update_fields=["number"])


class Migration(migrations.Migration):

    dependencies = [
        ("units", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="unit",
            name="code",
            field=models.CharField(blank=True, default="", max_length=40),
        ),
        migrations.AddField(
            model_name="unit",
            name="floor",
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name="unit",
            name="notes",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="unit",
            name="number",
            field=models.CharField(blank=True, default="", max_length=40),
        ),
        migrations.RunPython(populate_number_from_code, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="unit",
            name="number",
            field=models.CharField(max_length=40),
        ),
    ]
