# Generated by Django 3.2 on 2023-12-19 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0017_alter_resultimage_created'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='resultimage',
            name='created',
        ),
        migrations.AddField(
            model_name='resultimage',
            name='confirm_publish',
            field=models.BooleanField(default=False, help_text='Thick to Confirm Publish'),
        ),
    ]