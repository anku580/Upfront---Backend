# Generated by Django 2.0 on 2019-03-30 05:50

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=255, unique=True, verbose_name='username')),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_customer', models.BooleanField(default=True)),
                ('is_merchant', models.BooleanField(default=False)),
                ('is_subadmin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ConfirmAdmin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('status', models.BooleanField(default=False)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('admin', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='adminUser', to=settings.AUTH_USER_MODEL)),
                ('approved_admin', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='approved_admin', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ContactMedium',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Contact_type', models.PositiveSmallIntegerField(choices=[(1, 'Email'), (2, 'MobileNumber')], null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='contactUser', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('custEmail', models.EmailField(max_length=254, null=True)),
                ('customerId', models.AutoField(primary_key=True, serialize=False)),
                ('mobileNumber', models.BigIntegerField(null=True, validators=[django.core.validators.RegexValidator(message='Hashtag doesnt comply', regex='^[6-9]\\d{9}$')])),
                ('customer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Merchant',
            fields=[
                ('merchEmail', models.EmailField(max_length=254, null=True)),
                ('merchantId', models.AutoField(primary_key=True, serialize=False)),
                ('mobileNumber', models.BigIntegerField(null=True, validators=[django.core.validators.RegexValidator(message='Hashtag doesnt comply', regex='^[6-9]\\d{9}$')])),
                ('merchant', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SubAdmin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subEmail', models.EmailField(max_length=254, null=True)),
                ('mobileNumber', models.BigIntegerField(null=True, validators=[django.core.validators.RegexValidator(message='Hashtag doesnt comply', regex='^[6-9]\\d{9}$')])),
                ('merchant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myuser.Merchant')),
                ('subuser', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
