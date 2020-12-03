# Generated by Django 3.1.3 on 2020-12-03 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ContestPlus', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='applyDeadline',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='contest',
            name='applyStartTime',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='contest',
            name='censorStatus',
            field=models.CharField(blank=True, default='pending', max_length=16, null=True),
        ),
        migrations.AlterField(
            model_name='contest',
            name='contestDeadline',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='contest',
            name='contestStartTime',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='contest',
            name='reviewDeadline',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='contest',
            name='reviewStartTime',
            field=models.IntegerField(null=True),
        ),
    ]
