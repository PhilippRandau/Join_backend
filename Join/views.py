from django.http import Http404
from rest_framework import status, authentication, permissions, generics
from rest_framework.authtoken.views import ObtainAuthToken, APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializers import RegisterSerializer, TaskSerializer, CategorySerializer, AssignedToSerializer, SubtaskSerializer
from .models import Category, Task, Subtask
from django.contrib.auth import login
from django.contrib.auth.models import User, Group


class LoginView(ObtainAuthToken):
    permission_classes = []
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        email = request.data['email']
        password = request.data.get('password')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'Benutzer mit dieser E-Mail-Adresse existiert nicht'}, status=400)

        if user.check_password(password):
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.pk,
                'email': user.email
            })
        else:
            return Response({'error': 'Ungültiges Passwort'}, status=400)


class SignUpView(generics.CreateAPIView):
    permission_classes = []
    authentication_classes = []

    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class TaskView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        tasks = Task.objects.all()
        serializer = TaskSerializer(
            tasks, many=True, context={'request': request})
        return Response(serializer.data)

    def patch(self, request, format=None):
        try:
            task_id = request.data.get('id')
            task = Task.objects.get(id=task_id)
            serializer = TaskSerializer(
                task, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
        except Task.DoesNotExist:
            return Response({'error': 'Task not found'})

    def post(self, request, format=None):
        data = request.data

        serializer = TaskSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



class TasksDetailView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        try:
            task = Task.objects.get(pk=pk)
            serializer = TaskSerializer(task)
            return Response(serializer.data)
        except Task.DoesNotExist:
            raise Http404


class CategoryView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        categories = Category.objects.all()
        serializer = CategorySerializer(
            categories, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContactsView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        user = request.user
        contacts = User.objects.exclude(id=user.id)
        serializer = AssignedToSerializer(
            contacts, many=True, context={'request': request})
        return Response(serializer.data)


class SubtasksView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        subtasks = Subtask.objects.all()
        serializer = SubtaskSerializer(
            subtasks, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = SubtaskSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoggedInView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        user = request.user
        creator = User.objects.get(id=user.id)
        serializer = AssignedToSerializer(
            creator, many=False, context={'request': request})
        return Response(serializer.data)
