# Generated by Django 3.1.3 on 2020-12-12 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ContestPlus', '0006_auto_20201210_1617'),
    ]

    operations = [
        migrations.AddField(
            model_name='participation',
            name='submission',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
    ]
