# Generated by Django 3.1.3 on 2020-12-09 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ContestPlus', '0002_auto_20201209_1608'),
    ]

    operations = [
        migrations.AddField(
            model_name='participation',
            name='userId',
            field=models.IntegerField(default=0),
        ),
    ]
