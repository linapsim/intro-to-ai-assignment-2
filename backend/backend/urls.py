from django.urls import path
from backend.api.views import task_list, task_detail, register, login

urlpatterns = [
    path('tasks/', task_list),
    path('tasks/<int:pk>/', task_detail),
    path('register/', register),
    path('login/', login),
]