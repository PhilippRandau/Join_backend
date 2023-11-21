from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from Join import views

router = routers.DefaultRouter()
# router.register(r'tasks', views.TaskView)
# router.register(r'categorys', views.CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('login/', views.LoginView.as_view()),
    path('signup/', views.SignUpView.as_view()),
    path('tasks/', views.TaskView.as_view()),
    path('tasks/<int:pk>/', views.TasksDetailView.as_view()),
    path('categories/', views.CategoryView.as_view()),
    path('contacts/', views.ContactsView.as_view()),
    path('ownUser/', views.UserLoggedInView.as_view())
    
]

# urlpatterns = format_suffix_patterns(urlpatterns)