# Generated by Django 3.1.2 on 2020-11-23 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20201123_0400'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='Link',
            field=models.CharField(max_length=1000, null=True, unique=True),
        ),
    ]
