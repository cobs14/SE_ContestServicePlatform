# Generated by Django 3.1.3 on 2020-12-13 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ContestPlus', '0009_auto_20201213_0016'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='groupCode',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
    ]