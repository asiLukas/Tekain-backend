# Generated by Django 4.0.1 on 2022-02-12 11:36

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_message_room_name_alter_message_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 2, 12, 11, 36, 28, 691875, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='message',
            name='room_name',
            field=models.CharField(max_length=500, null=True),
        ),
    ]
