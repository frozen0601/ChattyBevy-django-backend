# Generated by Django 4.1.6 on 2023-02-25 04:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='room',
            options={'ordering': ['id']},
        ),
    ]
