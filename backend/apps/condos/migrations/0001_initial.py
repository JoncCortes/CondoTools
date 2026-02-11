from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Condominium',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('document', models.CharField(max_length=32, unique=True)),
                ('address', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('code', models.CharField(max_length=20)),
                ('block', models.CharField(blank=True, max_length=20)),
                ('condominium', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='condos.condominium')),
            ],
            options={'unique_together': {('condominium', 'code', 'block')}},
        ),
        migrations.CreateModel(
            name='CommonArea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('condominium', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='condos.condominium')),
            ],
        ),
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('published_at', models.DateTimeField(auto_now_add=True)),
                ('condominium', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='condos.condominium')),
            ],
        ),
        migrations.CreateModel(
            name='Visitor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('full_name', models.CharField(max_length=255)),
                ('document', models.CharField(max_length=32)),
                ('condominium', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='condos.condominium')),
                ('unit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='condos.unit')),
            ],
        ),
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('description', models.CharField(max_length=255)),
                ('received_at', models.DateTimeField(auto_now_add=True)),
                ('delivered_at', models.DateTimeField(blank=True, null=True)),
                ('condominium', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='condos.condominium')),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='packages', to='condos.unit')),
            ],
        ),
        migrations.CreateModel(
            name='Incident',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('status', models.CharField(default='OPEN', max_length=40)),
                ('condominium', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='condos.condominium')),
            ],
        ),
        migrations.CreateModel(
            name='VisitLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('entry_at', models.DateTimeField()),
                ('exit_at', models.DateTimeField(blank=True, null=True)),
                ('notes', models.TextField(blank=True)),
                ('condominium', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='condos.condominium')),
                ('visitor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='visit_logs', to='condos.visitor')),
            ],
        ),
        migrations.CreateModel(
            name='Resident',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('full_name', models.CharField(max_length=255)),
                ('phone', models.CharField(blank=True, max_length=20)),
                ('condominium', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='condos.condominium')),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='residents', to='condos.unit')),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('start_at', models.DateTimeField()),
                ('end_at', models.DateTimeField()),
                ('status', models.CharField(default='REQUESTED', max_length=40)),
                ('common_area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='condos.commonarea')),
                ('condominium', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='condos.condominium')),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='condos.unit')),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('full_name', models.CharField(max_length=255)),
                ('role_name', models.CharField(max_length=80)),
                ('condominium', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='condos.condominium')),
            ],
        ),
    ]
