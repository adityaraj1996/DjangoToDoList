from django.urls import path
from .views import TaskList, TaskDetail, TaskCreate, TaskUpdate, TaskDelete, CustomLoginView, register
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', TaskList.as_view(), name='tasks'),      # will look for model_list.html
    path('register/', register, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('task/<int:pk>/', TaskDetail.as_view(), name='task'),
    path('create-task/', TaskCreate.as_view(), name='create-task'),
    path('update-task/<int:pk>/', TaskUpdate.as_view(), name='update-task'),
    path('delete-task/<int:pk>/', TaskDelete.as_view(), name='delete-task'),
]