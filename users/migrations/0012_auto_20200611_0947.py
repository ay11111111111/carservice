# Generated by Django 3.0.6 on 2020-06-11 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_auto_20200611_0946'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='volume_dvigatel',
            field=models.IntegerField(choices=[('1.10', '1.10'), ('1.20', '1.20'), ('1.30', '1.30'), ('1.40', '1.40'), ('1.50', '1.50'), ('1.60', '1.60'), ('1.70', '1.70'), ('1.80', '1.80'), ('1.90', '1.90'), ('2.00', '2.00'), ('2.10', '2.10'), ('2.20', '2.20'), ('2.30', '2.30'), ('2.40', '2.40'), ('2.50', '2.50'), ('2.60', '2.60'), ('2.70', '2.70'), ('2.80', '2.80'), ('2.90', '2.90'), ('3.00', '3.00'), ('3.10', '3.10'), ('3.20', '3.20'), ('3.30', '3.30'), ('3.40', '3.40'), ('3.50', '3.50'), ('3.60', '3.60'), ('3.70', '3.70'), ('3.80', '3.80'), ('3.90', '3.90'), ('4.00', '4.00'), ('4.10', '4.10'), ('4.20', '4.20'), ('4.30', '4.30'), ('4.40', '4.40'), ('4.50', '4.50'), ('4.60', '4.60'), ('4.70', '4.70'), ('4.80', '4.80'), ('4.90', '4.90'), ('5.00', '5.00'), ('5.10', '5.10'), ('5.20', '5.20'), ('5.30', '5.30'), ('5.40', '5.40'), ('5.50', '5.50'), ('5.60', '5.60'), ('5.70', '5.70'), ('5.80', '5.80'), ('5.90', '5.90'), ('6.00', '6.00'), ('6.10', '6.10'), ('6.20', '6.20'), ('6.30', '6.30'), ('6.40', '6.40')], verbose_name='Объем двигателя'),
        ),
    ]
