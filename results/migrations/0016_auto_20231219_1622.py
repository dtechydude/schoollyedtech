# Generated by Django 3.2 on 2023-12-19 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0015_auto_20231219_1347'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='resultimage',
            options={'verbose_name': 'Thick The Box To Confirm Publish, - Please do not upload file'},
        ),
        migrations.RemoveField(
            model_name='resultimage',
            name='confirm_publish',
        ),
        migrations.AddField(
            model_name='resultimage',
            name='created',
            field=models.DateTimeField(auto_now=True),
        ),
    ]