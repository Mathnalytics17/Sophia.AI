# Generated by Django 3.0.4 on 2024-05-30 00:30

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0007_file_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='transaction_receipt',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
    ]