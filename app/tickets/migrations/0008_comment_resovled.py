# Generated by Django 5.1 on 2024-08-23 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0007_alter_category_options_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='resovled',
            field=models.BooleanField(default=False),
        ),
    ]
