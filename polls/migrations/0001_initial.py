
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Flote',
            fields=[
                ('type', models.CharField(choices=[('CAM', 'CAMIONETA'), ('RET', 'RETROESCAVADORA'), ('CAR', 'CARRETÓN'), ('MOT', 'MOTONIVELADORA'), ('CAO', 'CAMIÓN'), ('TAN', 'TANQUE DE COMBUSTIBLE'), ('TAR', 'TANQUE REGADOR')], max_length=50)),
                ('code', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('brand', models.CharField(max_length=50)),
                ('model', models.CharField(max_length=50)),
                ('characteristics', models.CharField(blank=True, max_length=600)),
                ('patent', models.CharField(blank=True, max_length=20)),
                ('production_year', models.IntegerField(blank=True, null=True)),
                ('engine_number', models.IntegerField(blank=True, null=True)),
                ('chassis_number', models.IntegerField(blank=True, null=True)),
                ('status', models.CharField(choices=[('GRE', 'VERDE'), ('YEL', 'AMARILLO'), ('RED', 'ROJO')], max_length=30)),
                ('justifyStatus', models.CharField(blank=True, default='', max_length=600)),
                ('operators', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=50), default=list, size=None)),
            ],
        ),
        migrations.CreateModel(
            name='Maintenance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('REP', 'REPAIR'), ('MAN', 'MAINTENANCE')], max_length=30)),
                ('date', models.DateField()),
                ('mileage', models.IntegerField()),
                ('description', models.CharField(max_length=600)),
                ('cost', models.FloatField()),
                ('flote', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.flote')),
            ],
            options={
                'ordering': ['date'],
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('flote', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.flote')),
            ],
        ),
    ]
