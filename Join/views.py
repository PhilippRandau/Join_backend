from django.http import Http404
from rest_framework import status, authentication, permissions, generics
from rest_framework.authtoken.views import ObtainAuthToken, APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializers import RegisterSerializer, TaskSerializer
from .models import Task
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

    # def post(self, request, *args, **kwargs):
    #     serializer = self.serializer_class(data=request.data,
    #                                        context={'request': request})
    #     serializer.is_valid(raise_exception=True)
    #     user = serializer.validated_data['user']
    #     token, created = Token.objects.get_or_create(user=user)
    #     return Response({
    #         'token': token.key,
    #         'user_id': user.pk,
    #         'email': user.email
    #     })
    def get(self, request, format=None):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)


class TasksDetailView(APIView):
    def get(self, request, pk):
        try:
            task = Task.objects.get(pk=pk)
            serializer = TaskSerializer(task)
            return Response(serializer.data)
        except Task.DoesNotExist:
            raise Http404
