# Generated by Django 2.2.6 on 2019-12-10 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodapp', '0009_auto_20191114_1653'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='link',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
