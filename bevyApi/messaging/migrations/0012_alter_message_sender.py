# Generated by Django 4.1.6 on 2023-02-16 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0011_alter_message_sender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='sender',
            field=models.CharField(default='aaa', max_length=100),
            preserve_default=False,
        ),
    ]