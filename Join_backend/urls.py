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
    path('categories/<int:pk>/', views.CategoryDetailView.as_view()),
    path('contacts/', views.ContactsView.as_view()),
    path('user/', views.UserView.as_view()),
    path('user/<int:pk>/', views.UsersDetailView.as_view()),
    path('subtasks/', views.SubtasksView.as_view()),
    path('subtasks/<int:pk>/', views.SubtaskDetailView.as_view()),
    path('summary/', views.SummaryView.as_view())
]