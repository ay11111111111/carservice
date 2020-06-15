# Generated by Django 3.0.6 on 2020-06-11 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_remove_car_volume_dvigatel'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='volume_dvigatel',
            field=models.DecimalField(choices=[(1.1, 1.1), (1.2, 1.2), (1.3, 1.3), (1.4, 1.4), (1.5, 1.5), (1.6, 1.6), (1.7, 1.7), (1.8, 1.8), (1.9, 1.9), (2.0, 2.0), (2.1, 2.1), (2.2, 2.2), (2.3, 2.3), (2.4, 2.4), (2.5, 2.5), (2.6, 2.6), (2.7, 2.7), (2.8, 2.8), (2.9, 2.9), (3.0, 3.0), (3.1, 3.1), (3.2, 3.2), (3.3, 3.3), (3.4, 3.4), (3.5, 3.5), (3.6, 3.6), (3.7, 3.7), (3.8, 3.8), (3.9, 3.9), (4.0, 4.0), (4.1, 4.1), (4.2, 4.2), (4.3, 4.3), (4.4, 4.4), (4.5, 4.5), (4.6, 4.6), (4.7, 4.7), (4.8, 4.8), (4.9, 4.9), (5.0, 5.0), (5.1, 5.1), (5.2, 5.2), (5.3, 5.3), (5.4, 5.4), (5.5, 5.5), (5.6, 5.6), (5.7, 5.7), (5.8, 5.8), (5.9, 5.9), (6.0, 6.0), (6.1, 6.1), (6.2, 6.2), (6.3, 6.3), (6.4, 6.4)], decimal_places=1, default=0, max_digits=3, verbose_name='Объем двигателя'),
            preserve_default=False,
        ),
    ]
