# Generated by Django 5.1.3 on 2024-11-14 11:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Questionbank', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='updated_at',
        ),
    ]