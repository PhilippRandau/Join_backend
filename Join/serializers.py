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
        model=User
        fields = ['id', 'first_name', 'last_name']

class CreatorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=User
        fields = ['id', 'username']

class SubtaskSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Subtask
        fields = ['title', 'completed']  # 'example_time_passed'

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ['title', 'created_at', 'category_color']

# class GroupSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Group
#         fields = ['url', 'name']


class TaskSerializer(serializers.HyperlinkedModelSerializer):
    creator = CreatorSerializer(
        read_only=True, default=serializers.CurrentUserDefault())

    assigned_to = AssignedToSerializer(many=True, read_only=True)
    subtasks = SubtaskSerializer(many=True, read_only=True)
    category = CategorySerializer(many=False, read_only=True)


    class Meta:
        model = Task
        fields = ['id', 'section', 'title', 'description','category', 'assigned_to',
                  'created_at', 'due_date', 'prio',  'subtasks', 'creator',]  # 'example_time_passed'


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
