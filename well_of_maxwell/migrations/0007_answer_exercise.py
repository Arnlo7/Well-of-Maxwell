# Generated by Django 4.0.3 on 2023-03-16 00:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('well_of_maxwell', '0006_remove_image_active_remove_image_orientation_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(default='', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(default='', max_length=200)),
                ('answers', models.ManyToManyField(related_name='answer_exercise', to='well_of_maxwell.answer')),
                ('correct', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='well_of_maxwell.answer')),
            ],
        ),
    ]