# Generated by Django 4.0.3 on 2023-02-13 22:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('well_of_maxwell', '0004_content_guest_remove_module_content_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='content',
            name='active',
        ),
        migrations.RemoveField(
            model_name='text',
            name='active',
        ),
        migrations.RemoveField(
            model_name='text',
            name='orientation',
        ),
    ]
