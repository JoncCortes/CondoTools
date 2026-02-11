from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='MenuCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('order', models.PositiveIntegerField(default=0)),
            ],
            options={'ordering': ['order', 'name']},
        ),
        migrations.CreateModel(
            name='CustomPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(unique=True)),
                ('content', models.TextField(blank=True)),
                ('allowed_roles', models.JSONField(blank=True, default=list)),
                ('enabled', models.BooleanField(default=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='custom_pages', to='settings_menu.menucategory')),
            ],
            options={'ordering': ['title']},
        ),
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.SlugField(max_length=80, unique=True)),
                ('label', models.CharField(max_length=120)),
                ('path', models.CharField(max_length=200)),
                ('order', models.PositiveIntegerField(default=0)),
                ('enabled', models.BooleanField(default=True)),
                ('allowed_roles', models.JSONField(blank=True, default=list)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='items', to='settings_menu.menucategory')),
            ],
            options={'ordering': ['order', 'id']},
        ),
    ]
