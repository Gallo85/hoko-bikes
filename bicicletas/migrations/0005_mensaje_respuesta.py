# Generated by Django 5.1.3 on 2024-12-30 02:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bicicletas', '0004_mensaje'),
    ]

    operations = [
        migrations.AddField(
            model_name='mensaje',
            name='respuesta',
            field=models.TextField(blank=True, null=True),
        ),
    ]