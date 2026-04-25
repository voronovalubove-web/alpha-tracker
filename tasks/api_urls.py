from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'projects', views.ProjectViewSet, basename='project')
router.register(r'tasks', views.TaskViewSet, basename='task')
router.register(r'users', views.UserViewSet, basename='user')

urlpatterns = [
    path('users/me/', views.CurrentUserView.as_view(), name='current-user'),
    path('', include(router.urls)),  
]