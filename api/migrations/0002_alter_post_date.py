# Generated by Django 4.0.1 on 2022-02-02 19:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 2, 2, 19, 28, 23, 835622)),
        ),
    ]