# Generated by Django 3.0.2 on 2020-08-29 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ville', '0002_auto_20200826_1136'),
    ]

    operations = [
        migrations.AddField(
            model_name='noms',
            name='creation',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='noms',
            name='verification',
            field=models.BooleanField(default=False),
        ),
    ]