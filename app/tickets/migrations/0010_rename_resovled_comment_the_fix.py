# Generated by Django 5.1 on 2024-08-23 15:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0009_remove_ticket_resolution'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='resovled',
            new_name='the_fix',
        ),
    ]