# Generated by Django 2.0 on 2019-03-30 05:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('menu_app', '0001_initial'),
        ('restaurant_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('price', models.FloatField()),
                ('res_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurant_app.Restaurant')),
            ],
        ),
        migrations.CreateModel(
            name='MenuCustomization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customization_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customization_app.Customization')),
                ('menu_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='menu_app.Menu')),
            ],
        ),
    ]