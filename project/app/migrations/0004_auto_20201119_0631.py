# Generated by Django 3.1.2 on 2020-11-19 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20201119_0627'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='Link',
            field=models.CharField(max_length=100),
        ),
    ]
