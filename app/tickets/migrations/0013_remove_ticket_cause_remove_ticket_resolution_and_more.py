# Generated by Django 5.1 on 2024-09-28 09:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0012_rename_fix_ticket_resolution'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='cause',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='resolution',
        ),
        migrations.CreateModel(
            name='TicketSolution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cause', models.TextField()),
                ('solution', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='solutions', to='tickets.ticket')),
            ],
        ),
    ]
