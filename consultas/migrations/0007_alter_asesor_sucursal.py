# Generated by Django 4.2.18 on 2025-01-16 16:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('consultas', '0006_delete_asociado_asesor_sucursal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asesor',
            name='sucursal',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='consultas.sucursal'),
        ),
    ]
