# Generated by Django 3.0.4 on 2024-05-13 23:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0004_file_hash'),
    ]

    operations = [
        migrations.RenameField(
            model_name='file',
            old_name='hash',
            new_name='text_hash',
        ),
        migrations.AddField(
            model_name='file',
            name='extracted_text',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='file',
            name='text_length',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]