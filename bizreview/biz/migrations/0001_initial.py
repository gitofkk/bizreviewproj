# Generated by Django 2.1 on 2018-08-30 13:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.crypto
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cities', '0011_auto_20180108_0706'),
        migrations.swappable_dependency(settings.CITIES_COUNTRY_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flat_no', models.CharField(max_length=200)),
                ('building_name', models.CharField(max_length=200)),
                ('street', models.CharField(max_length=200)),
                ('area', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=200)),
                ('postcode', models.CharField(max_length=200)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.CITIES_COUNTRY_MODEL)),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cities.Region')),
            ],
        ),
        migrations.CreateModel(
            name='Complaint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('published_date', models.DateTimeField(blank=True, null=True)),
                ('verify_code', models.CharField(default=django.utils.crypto.get_random_string, max_length=200)),
                ('is_active', models.BooleanField(default=False)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='biz.Address')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='complaint',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='biz.User'),
        ),
    ]