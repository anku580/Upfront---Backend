# Generated by Django 2.0 on 2019-04-03 05:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('temperorycart', '0006_auto_20190402_1308'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartmenucustomization',
            name='customization',
        ),
    ]
