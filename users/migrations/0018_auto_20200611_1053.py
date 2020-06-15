# Generated by Django 3.0.6 on 2020-06-11 10:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0017_remove_car_volume_dvigatel'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='car_model',
            field=models.CharField(default='', max_length=60),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='car',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
