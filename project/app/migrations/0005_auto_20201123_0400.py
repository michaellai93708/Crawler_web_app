# Generated by Django 3.1.2 on 2020-11-23 04:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20201119_0631'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='Link',
            field=models.CharField(max_length=1000, unique=True),
        ),
    ]
