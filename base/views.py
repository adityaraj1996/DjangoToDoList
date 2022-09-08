from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Task
from django.urls import reverse_lazy

# Create your views here.


class TaskList(ListView):
    model = Task
    context_object_name = 'tasks'                        #object_list is the default name
                                                        # will look for model(lower_case)_list.html


class TaskDetail(DetailView):
    model = Task                                        # will look for model(lower_case)_detail.html
    context_object_name = 'task'                        # object is the default name
    template_name = 'base/task.html'


class TaskCreate(CreateView):
    model = Task                                        # will look for model(lower_case)_form.html
    fields = '__all__'
    success_url = reverse_lazy('tasks')


class TaskUpdate(UpdateView):
    model = Task                                        # will look for model(lower_case)_form.html
    fields = '__all__'
    success_url = reverse_lazy('tasks')


class TaskDelete(DeleteView):
    model = Task                                           # will look for model(lower_case)_confirm_delete.html
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')
