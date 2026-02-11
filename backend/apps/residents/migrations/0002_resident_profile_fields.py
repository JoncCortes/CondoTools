from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('residents', '0001_initial'),
    ]

    operations = [
        migrations.AddField(model_name='resident', name='document', field=models.CharField(blank=True, max_length=30)),
        migrations.AddField(model_name='resident', name='notes', field=models.TextField(blank=True)),
        migrations.AddField(model_name='resident', name='photo_url', field=models.URLField(blank=True)),
        migrations.AddField(model_name='resident', name='status', field=models.CharField(default='ACTIVE', max_length=30)),
    ]
