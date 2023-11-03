import datetime
from django.db import models
from colorfield.fields import ColorField
# from django.contrib.auth.models import User, Group


class Category(models.Model):
    title = models.CharField(max_length=30)
    created_at = models.DateField(default=datetime.date.today)
    category_color = ColorField(default='#FF0000')

    def __str__(self) -> str:
        return self.title
    
class Task(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
    created_at = models.DateField(default=datetime.date.today)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        default=None
    )
    due_date = models.DateField(default=datetime.date.today)
    # assigned_to = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Task')
    # user = models.ForeignKey(
    #     User,
    #     on_delete=models.CASCADE,
    #     default=None
    # )

    def __str__(self) -> str:
        return f'({self.id}) {self.title}'

    def example_time_passed(self):
        today = datetime.date.today()
        delta = today - self.created_at
        return delta.days
    