# Generated by Django 2.2.6 on 2020-04-15 02:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodapp', '0011_auto_20200412_1441'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='Essential_ingredient',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='ingredient_test'),
        ),
    ]