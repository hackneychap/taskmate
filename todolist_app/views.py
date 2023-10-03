from django.shortcuts import render, redirect
from django.http import HttpResponse
from todolist_app.models import TaskList
from todolist_app.forms import Taskform
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

@login_required
def todolist(request):
    if request.method == "POST":
        form = Taskform(request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.manage = request.user
            instance.save()
        messages.success(request,("New Task"))
        return redirect ('todolist')
    else:
        all_task = TaskList.objects.filter(manage=request.user)
        paginator = Paginator(all_task, 10)
        page = request.GET.get('pg')
        all_task = paginator.get_page(page)
        
        return render(request, "todolist.html", {'all_tasks' : all_task})

def contact(request):
    context = {
        'contact_text': "welcome to contact.",
        }
    return render(request, "contact.html", context)

def index(request):
    context = {
        'index_text': "welcome to index.",
        }
    return render(request, "index.html", context)

def about(request):
    context = {
        'about_text': "welcome to about.",
        }
    return render(request, "about.html", context)

@login_required
def delete_task(request, task_id):
    task = TaskList.objects.get(pk=task_id)
    if task.manage == request.user:
        task.delete()
    else:
        messages.success(request,("Task not found."))
    return redirect('todolist')

@login_required
def complete_task(request, task_id):
    task = TaskList.objects.get(pk=task_id)
    if task.manage == request.user:
        task.done = True
        task.save()
    else:
        messages.success(request,("Task not found."))
    return redirect('todolist')

@login_required
def pending_task(request, task_id):
    task = TaskList.objects.get(pk=task_id)
    task.done = False
    task.save()
    return redirect('todolist')

@login_required
def edit_task(request, task_id):
    if request.method == "POST":
        task = TaskList.objects.get(pk=task_id)
        form = Taskform(request.POST or None, instance = task)
        if form.is_valid():
            form.save()
        messages.success(request,("New Task Edited!"))
        return redirect ('todolist')
    else:
        task_obj = TaskList.objects.get(pk=task_id)
        return render(request, "edit.html", {'task_obj' : task_obj})


