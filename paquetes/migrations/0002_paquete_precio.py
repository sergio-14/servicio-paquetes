# Generated by Django 5.1.4 on 2024-12-05 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paquetes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='paquete',
            name='precio',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
            preserve_default=False,
        ),
    ]
