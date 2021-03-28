# Generated by Django 3.1.7 on 2021-03-28 10:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Dataset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('csv_file', models.FileField(blank=True, null=True, upload_to='datasets/')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Schema',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('column_separator', models.CharField(choices=[(',', 'Comma'), (';', 'Semicolon')], default=',', max_length=1)),
                ('string_character', models.CharField(choices=[("'", 'Single quotes'), ('"', 'Double quotes')], default="'", max_length=1)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schemas', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SchemaColumn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('column_name', models.CharField(max_length=255)),
                ('type', models.CharField(choices=[('job', 'Job'), ('company', 'Company'), ('full_name', 'Full Name'), ('phone', 'Phone'), ('address', 'Address'), ('email', 'Email'), ('domain_name', 'Domain name'), ('date', 'Date')], default='job', max_length=255)),
                ('schema', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='columns', to='csv_maker.schema')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
