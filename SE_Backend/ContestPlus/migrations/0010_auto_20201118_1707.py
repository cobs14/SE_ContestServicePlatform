# Generated by Django 3.1.1 on 2020-11-18 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ContestPlus', '0009_auto_20201118_1659'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contest',
            old_name='sponserId',
            new_name='sponsorId',
        ),
        migrations.AddField(
            model_name='contest',
            name='abstract',
            field=models.CharField(blank=True, max_length=512),
        ),
    ]