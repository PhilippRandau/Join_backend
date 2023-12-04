import datetime
from django.db import models
from colorfield.fields import ColorField
from django.contrib.auth.models import User, Group
from rest_framework import serializers
from django.db.models.signals import post_save
from django.dispatch import receiver
import random


def get_random_color():
    color_options = ['#ffa500', '#F44336', '#9C27B0',
                     '#3F51B5', '#2196F3', '#00BCD4', '#4CAF50', '#FF9800']
    return random.choice(color_options)


class UserDetail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bubble_color = ColorField(default=get_random_color)

    def __str__(self) -> str:
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserDetail.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_userdetail(sender, instance, **kwargs):
    instance.userdetail.save()


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
        max_length=17, choices=TASK_SECTIONS, default="To_Do")
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
