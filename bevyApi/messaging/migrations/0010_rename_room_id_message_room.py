# Generated by Django 4.1.6 on 2023-02-09 00:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0009_alter_message_room_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='room_id',
            new_name='room',
        ),
    ]
