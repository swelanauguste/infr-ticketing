# Generated by Django 5.1 on 2024-09-28 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0020_alter_ticketassignment_assigned_to_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ticketassignment',
            options={'ordering': ['-created_at']},
        ),
        migrations.AlterModelOptions(
            name='ticketsolution',
            options={'ordering': ['-created_at']},
        ),
        migrations.RenameField(
            model_name='ticketassignment',
            old_name='assigned_to',
            new_name='assign_to',
        ),
        migrations.AlterField(
            model_name='ticket',
            name='status',
            field=models.CharField(choices=[('open', 'Open'), ('on_hold', 'On Hold'), ('resolved', 'Resolved')], default='open', max_length=20),
        ),
    ]