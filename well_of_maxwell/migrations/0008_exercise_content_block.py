# Generated by Django 4.0.3 on 2023-03-16 01:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('well_of_maxwell', '0007_answer_exercise'),
    ]

    operations = [
        migrations.AddField(
            model_name='exercise',
            name='content_block',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='well_of_maxwell.content'),
        ),
    ]
