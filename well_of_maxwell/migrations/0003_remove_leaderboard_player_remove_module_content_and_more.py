# Generated by Django 4.0.3 on 2023-02-13 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('well_of_maxwell', '0002_content_image_text_module_content_image_content_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='leaderboard',
            name='player',
        ),
        migrations.RemoveField(
            model_name='module',
            name='content',
        ),
        migrations.AddField(
            model_name='module',
            name='content',
            field=models.CharField(default='', max_length=1000),
        ),
        migrations.AlterField(
            model_name='module',
            name='page_title',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.DeleteModel(
            name='Content',
        ),
        migrations.DeleteModel(
            name='Guest',
        ),
        migrations.DeleteModel(
            name='Image',
        ),
        migrations.DeleteModel(
            name='Leaderboard',
        ),
        migrations.DeleteModel(
            name='Text',
        ),
    ]