# Generated by Django 4.0.6 on 2023-11-24 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Join', '0004_alter_task_section'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='section',
            field=models.CharField(choices=[('To_Do', 'To Do'), ('In_Progress', 'In Progress'), ('Awaiting_Feedback', 'Awaiting Feedback'), ('Done', 'Done')], default='To_Do', max_length=17),
        ),
    ]
