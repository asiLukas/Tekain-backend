# Generated by Django 4.0.1 on 2022-02-12 11:36

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0019_alter_post_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 2, 12, 11, 36, 46, 12843, tzinfo=utc)),
        ),
    ]
