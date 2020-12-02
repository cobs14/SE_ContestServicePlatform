# Generated by Django 3.1.3 on 2020-12-02 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256)),
                ('abstract', models.CharField(blank=True, max_length=512)),
                ('description', models.TextField(blank=True)),
                ('module', models.CharField(max_length=256)),
                ('link', models.CharField(blank=True, max_length=256, null=True)),
                ('thumb', models.CharField(blank=True, max_length=218, null=True)),
                ('sponsorId', models.IntegerField(default=0)),
                ('allowGroup', models.BooleanField(default=False)),
                ('maxGroupMember', models.IntegerField(default=1)),
                ('minGroupMember', models.IntegerField(default=1)),
                ('censorStatus', models.CharField(default='pending', max_length=16)),
                ('applyStartTime', models.DateTimeField()),
                ('applyDeadline', models.DateTimeField()),
                ('contestStartTime', models.DateTimeField()),
                ('contestDeadline', models.DateTimeField()),
                ('reviewStartTime', models.DateTimeField()),
                ('reviewDeadline', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Counter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('value', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='EmailCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userType', models.CharField(max_length=16)),
                ('userId', models.CharField(max_length=16)),
                ('code', models.CharField(max_length=8)),
                ('sendTime', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('description', models.CharField(max_length=256)),
                ('memberCount', models.IntegerField()),
                ('memberId', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contestId', models.IntegerField()),
                ('link', models.CharField(max_length=512)),
                ('content', models.TextField()),
                ('title', models.CharField(max_length=128)),
                ('file', models.CharField(max_length=512)),
                ('hostType', models.CharField(default='none', max_length=16)),
                ('hostId', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Participation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(default='single', max_length=16)),
                ('participantId', models.IntegerField(default=0)),
                ('targetContestId', models.IntegerField(default=0)),
                ('checkStatus', models.CharField(default='pending', max_length=16)),
                ('completeStatus', models.CharField(default='ready', max_length=16)),
                ('grade', models.IntegerField(default=0)),
                ('fullGrade', models.IntegerField(default=100)),
                ('awardTitle', models.CharField(blank=True, max_length=256)),
                ('awardContent', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture_id', models.IntegerField()),
                ('url', models.CharField(max_length=128)),
                ('hostType', models.CharField(default='none', max_length=16)),
                ('hostId', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=32)),
                ('password', models.CharField(max_length=256)),
                ('email', models.EmailField(max_length=64)),
                ('emailVerifyStatus', models.BooleanField(default=False)),
                ('userType', models.CharField(default='user', max_length=16)),
                ('loginStatus', models.BooleanField(default=False)),
                ('pubKey', models.CharField(blank=True, max_length=512)),
                ('priKey', models.CharField(blank=True, max_length=512)),
                ('jwt', models.CharField(blank=True, max_length=512)),
                ('avatar', models.CharField(blank=True, max_length=128)),
                ('qualificationStatus', models.CharField(default='guest', max_length=16)),
                ('OutdateTime', models.DateTimeField(blank=True, null=True)),
                ('documentNumberNeeded', models.BooleanField(blank=True, default=True)),
                ('documentNumber', models.CharField(blank=True, max_length=32)),
                ('trueName', models.CharField(blank=True, max_length=32)),
                ('birthTime', models.DateField(blank=True, null=True)),
            ],
        ),
    ]
