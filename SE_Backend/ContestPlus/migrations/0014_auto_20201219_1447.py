# Generated by Django 3.1.3 on 2020-12-19 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ContestPlus', '0013_auto_20201216_1630'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participation',
            name='grade',
            field=models.CharField(default='', max_length=16),
        ),
    ]
