# Generated by Django 3.2 on 2023-09-07 00:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SchoolDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=150)),
                ('slogan', models.CharField(blank=True, max_length=150)),
                ('address', models.CharField(blank=True, max_length=150)),
                ('phone', models.CharField(blank=True, max_length=150)),
                ('email', models.CharField(blank=True, max_length=150)),
                ('website', models.CharField(blank=True, max_length=150)),
            ],
        ),
    ]