from django.shortcuts import render, redirect, HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Task
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from .form import UserRegisterForm
from django.contrib import messages

from django.views import View
from django.shortcuts import redirect
from django.db import transaction

from .models import Task
from .form import PositionForm

# Create your views here.


def register(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = UserRegisterForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                messages.success(request, f"Account created for {username}")
                return redirect('login')
        else:
            form = UserRegisterForm()
        return render(request, "base/register.html", {"form": form})
    return HttpResponse("already logged in..")

    # if request.method == 'POST':
    #     form = UserRegisterForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         username = form.cleaned_data.get('username')
    #         messages.success(request, f"Account created for {username}")
    #         return redirect('login')
    # else:
    #     form = UserRegisterForm()
    # return render(request, "base/register.html", {"form": form})


class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')


class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'                        #object_list is the default name
                                                        # will look for model(lower_case)_list.html
    # getting user specific data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        search_input = self.request.GET.get('search-area')
        if search_input:
            context['tasks'] = context['tasks'].filter(title__icontains=search_input)
        context['search_input'] = search_input
        return context


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task                                        # will look for model(lower_case)_detail.html
    context_object_name = 'task'                        # object is the default name
    template_name = 'base/task.html'


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task                                        # will look for model(lower_case)_form.html
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):                    # coz user is meaningless to show if logged in
        form.instance.user = self.request.user
        return super().form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task                                        # will look for model(lower_case)_form.html
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task                                           # will look for model(lower_case)_confirm_delete.html
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')


class TaskReorder(View):
    def post(self, request):
        form = PositionForm(request.POST)

        if form.is_valid():
            positionList = form.cleaned_data["position"].split(',')

            with transaction.atomic():
                self.request.user.set_task_order(positionList)

        return redirect(reverse_lazy('tasks'))
