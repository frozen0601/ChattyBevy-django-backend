# Generated by Django 4.1.6 on 2023-02-09 00:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0004_alter_message_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user1', models.CharField(max_length=100)),
                ('user2', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='message',
            name='r_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='messaging.room'),
            preserve_default=False,
        ),
    ]
