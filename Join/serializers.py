from django.contrib.auth.models import User, Group
from rest_framework import serializers
from Join.models import Task, Category, Subtask
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password



class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class AssignedToSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name']


class CreatorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class SubtaskSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Subtask
        fields = ['title', 'completed']  # 'example_time_passed'


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'created_at', 'category_color']


class TaskSerializer(serializers.HyperlinkedModelSerializer):
    creator = CreatorSerializer(
        read_only=True, default=serializers.CurrentUserDefault())

    assigned_to = AssignedToSerializer(many=True)
    subtasks = SubtaskSerializer(many=True, read_only=True)
    category = CategorySerializer(many=False)

    class Meta:
        model = Task
        fields = ['id', 'section', 'title', 'description', 'category', 'assigned_to',
                  'created_at', 'due_date', 'prio',  'subtasks', 'creator',]  # 'example_time_passed'
        
    def create(self, validated_data, *args, **kwargs):
        category_data = validated_data.pop('category')
        category_instance = Category.objects.get(**category_data)
        validated_data['category'] = category_instance
        

        assigned_to_data = validated_data.pop('assigned_to', [])
        assigned_to_instances = []

        for user_data in assigned_to_data:
            user_instance = User.objects.get(**user_data)
            assigned_to_instances.append(user_instance)

        validated_data['assigned_to'] = assigned_to_instances

        validated_data['creator'] = self.context['request'].user

        return super(TaskSerializer, self).create(validated_data, *args, **kwargs)

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2',
                  'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user
