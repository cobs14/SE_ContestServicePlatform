# Generated by Django 3.1.3 on 2020-12-13 00:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ContestPlus', '0008_auto_20201212_2355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participation',
            name='submissionDir',
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
    ]
