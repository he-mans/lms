# Generated by Django 2.2.5 on 2019-11-17 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='description',
            field=models.CharField(default='No description provided by teacher', max_length=500),
        ),
    ]
