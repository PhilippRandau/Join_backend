import datetime
from django.db import models
from colorfield.fields import ColorField
from django.contrib.auth.models import User, Group
from rest_framework import serializers


class Category(models.Model):
    title = models.CharField(max_length=30)
    created_at = models.DateField(default=datetime.date.today)
    category_color = ColorField(default='#FF0000')

    def __str__(self) -> str:
        return self.title


class Subtask(models.Model):
    title = models.CharField(max_length=100)
    completed = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title


class Task(models.Model):
    TASK_PRIOS = [
        ("Low", "Low"),
        ("Medium", "Medium"),
        ("Urgent", "Urgent")
    ]
    TASK_SECTIONS = [
        ("To_Do", "To Do"),
        ("In_Progress", "In Progress"),
        ("Awaiting_Feedback", "Awaiting Feedback"),
        ("Done", "Done")
    ]
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
    created_at = models.DateField(default=datetime.date.today)
    due_date = models.DateField(default=datetime.date.today)
    prio = models.CharField(max_length=6, choices=TASK_PRIOS, default="Low")
    section = models.CharField(
        max_length=17, choices=TASK_SECTIONS, default="Todo")
    assigned_to = models.ManyToManyField(User, related_name='assigned_to')
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        default=None
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        default=None
    )
    subtasks = models.ManyToManyField(Subtask, related_name='subtasks')

    def __str__(self) -> str:
        return f'({self.id}) {self.title}'

    def example_time_passed(self):
        today = datetime.date.today()
        delta = today - self.created_at
        return delta.days
