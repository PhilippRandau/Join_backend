from django.contrib.auth.models import User, Group
from rest_framework import serializers

from Join.models import Task, Category


# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'first_name', 'last_name', 'email']


# class TaskSerializer(serializers.HyperlinkedModelSerializer):
#     user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
#     class Meta:
#         model = Task
#         fields = ['id', 'title', 'description', 'created_at', 'user', 'example_time_passed']


# class CategorySerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Category
#         fields = ['title', 'created_at', 'category_color']
