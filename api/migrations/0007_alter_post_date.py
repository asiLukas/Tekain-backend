# Generated by Django 4.0.1 on 2022-02-03 21:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_alter_post_date_alter_post_file_alter_post_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 2, 3, 21, 18, 10, 227103)),
        ),
    ]
