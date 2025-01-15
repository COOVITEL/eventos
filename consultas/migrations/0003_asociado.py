# Generated by Django 4.2.18 on 2025-01-15 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consultas', '0002_asesor_sucursal'),
    ]

    operations = [
        migrations.CreateModel(
            name='Asociado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('documento', models.CharField(max_length=200)),
                ('state', models.CharField(max_length=100)),
                ('descripcion', models.CharField(max_length=500)),
                ('causa', models.CharField(max_length=200)),
            ],
        ),
    ]
