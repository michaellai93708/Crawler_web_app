# Generated by Django 3.1.2 on 2020-11-23 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20201123_0836'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='Title',
            field=models.CharField(max_length=1000),
        ),
    ]
