# Generated by Django 4.2.18 on 2025-01-14 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EntregaObsequio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('documento', models.CharField(max_length=200)),
                ('sucursal', models.CharField(max_length=200)),
                ('estado', models.CharField(max_length=200)),
                ('obsequio', models.CharField(max_length=200)),
                ('asesor', models.CharField(max_length=200)),
                ('razonDeEntrega', models.CharField(blank=True, max_length=1000, null=True)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
