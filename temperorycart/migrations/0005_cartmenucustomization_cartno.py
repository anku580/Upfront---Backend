# Generated by Django 2.0 on 2019-04-02 11:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('temperorycart', '0004_cartmenucustomization_customuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartmenucustomization',
            name='cartNo',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='customorderno', to='temperorycart.Cart'),
            preserve_default=False,
        ),
    ]
