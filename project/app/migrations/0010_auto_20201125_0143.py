# Generated by Django 3.1.2 on 2020-11-25 01:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_auto_20201123_0919'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='Author',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]
