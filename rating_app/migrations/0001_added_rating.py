# Generated by Django 2.0 on 2019-04-01 12:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('temperorycart', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.FloatField()),
                ('msg', models.CharField(max_length=500)),
                ('order_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='temperorycart.Order')),
            ],
        ),
    ]
