# Generated by Django 3.1.1 on 2020-11-19 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ContestPlus', '0010_auto_20201118_1707'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='title',
            field=models.CharField(max_length=256),
        ),
    ]
