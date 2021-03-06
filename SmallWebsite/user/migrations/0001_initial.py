# Generated by Django 2.1.2 on 2018-12-05 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserRegister',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_number', models.CharField(max_length=11, unique=True)),
                ('password', models.CharField(max_length=200)),
                ('level', models.IntegerField(default=0)),
                ('scores', models.IntegerField(default=0)),
                ('portrait', models.ImageField(default='portrait/', upload_to='')),
                ('mini_name', models.CharField(max_length=50)),
                ('times', models.IntegerField(default=0)),
            ],
        ),
    ]
