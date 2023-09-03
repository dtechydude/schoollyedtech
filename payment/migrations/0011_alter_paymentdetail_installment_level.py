# Generated by Django 3.2 on 2023-09-03 00:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0010_alter_paymentdetail_installment_level'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentdetail',
            name='installment_level',
            field=models.CharField(choices=[('First_payment', 'First_payment'), ('Second_payment', 'Second_payment'), ('Third_payment', 'Third_payment'), ('Fourth_payment', 'Fourth_payment'), ('Complete_once', 'Complete_once')], default='select_installment', max_length=50),
        ),
    ]