# Generated by Django 3.1.3 on 2020-12-19 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ContestPlus', '0014_auto_20201219_1447'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='idNumber',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='contest',
            name='publishResult',
            field=models.CharField(default='', max_length=12),
        ),
    ]
