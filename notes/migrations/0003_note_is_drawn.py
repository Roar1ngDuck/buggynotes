# Generated by Django 4.2.7 on 2023-11-07 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0002_note_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='is_drawn',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
