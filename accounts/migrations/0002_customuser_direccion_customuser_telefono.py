# Generated by Django 5.1.3 on 2024-12-27 23:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='direccion',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='telefono',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
