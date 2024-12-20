# Generated by Django 5.1.3 on 2024-11-14 08:34

import django_jalali.db.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
                ('Question_description', models.CharField(max_length=3000000000000)),
                ('date', django_jalali.db.models.jDateField(auto_now_add=True)),
                ('choice', models.CharField(choices=[('easy', 'آسان'), ('normal', 'متوسط'), ('hard', 'سخت')], max_length=11)),
                ('updated_at', django_jalali.db.models.jDateField(auto_now_add=True)),
            ],
        ),
    ]
