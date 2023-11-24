from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from Join import views

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('login/', views.LoginView.as_view()),
    path('signup/', views.SignUpView.as_view()),
    path('tasks/', views.TaskView.as_view()),
    path('tasks/<int:pk>/', views.TasksDetailView.as_view()),
    path('categories/', views.CategoryView.as_view()),
    path('contacts/', views.ContactsView.as_view()),
    path('ownUser/', views.UserLoggedInView.as_view()),
    path('subtasks/', views.SubtasksView.as_view()),
]