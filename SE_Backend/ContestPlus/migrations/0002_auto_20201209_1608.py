# Generated by Django 3.1.3 on 2020-12-09 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ContestPlus', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='major',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='school',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='schoolNumber',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]