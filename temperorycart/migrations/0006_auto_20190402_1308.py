# Generated by Django 2.0 on 2019-04-02 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customization_app', '0001_initial'),
        ('temperorycart', '0005_cartmenucustomization_cartno'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartmenucustomization',
            name='customization',
        ),
        migrations.AddField(
            model_name='cartmenucustomization',
            name='customization',
            field=models.ManyToManyField(to='customization_app.Customization'),
        ),
    ]
