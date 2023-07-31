# Generated by Django 3.2 on 2023-07-27 11:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('curriculum', '0002_classgroup'),
        ('staff', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='staffprofile',
            name='class_group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='curriculum.classgroup'),
        ),
    ]
