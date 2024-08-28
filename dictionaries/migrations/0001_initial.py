# Generated by Django 5.1 on 2024-08-27 07:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dictionary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100, unique=True)),
                ('name', models.CharField(max_length=300)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='DictionaryVersion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.CharField(max_length=50)),
                ('start_date', models.DateField()),
                ('dictionary', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='versions', to='dictionaries.dictionary')),
            ],
            options={
                'unique_together': {('dictionary', 'version', 'start_date')},
            },
        ),
        migrations.CreateModel(
            name='DictionaryElement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100)),
                ('value', models.CharField(max_length=300)),
                ('version', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='elements', to='dictionaries.dictionaryversion')),
            ],
            options={
                'unique_together': {('version', 'code')},
            },
        ),
    ]
