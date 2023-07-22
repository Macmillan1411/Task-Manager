
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Task, TaskHistory
from .forms import TaskForm

# Create your views here.
@login_required
def task_list(request):
    tasks = Task.objects.filter(owner=request.user).order_by('-created_at').distinct()
    return render(request, 'task_list.html', {'tasks': tasks})

@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk, owner=request.user)
    return render(request, 'task_detail.html', {'task': task})

@login_required
def task_new(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.owner = request.user
            task.save()
            #TaskHistory.create(task,action='created')
            return redirect('tasks:task_detail', pk=task.pk)
    else:
        form = TaskForm()
    return render(request, 'task_edit.html', {'form': form})

@login_required
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            task.updated_by = request.user
            task.save()
            #TaskHistory.create(task,action='updated')
            return redirect('tasks:task_detail', pk=task.pk)
    else:
        form =TaskForm(instance=task)
    return render(request, 'task_edit.html', {'form': form})

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, owner=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks:task_list')
    return render(request, 'task_delete.html', {'task': task})

@login_required
def task_history(request, pk):
    task = get_object_or_404(Task, pk=pk, owner=request.user)
    task_history = TaskHistory.objects.filter(task=task).order_by('-timestamp')
    return render(request, 'task_history.html', {'task': task, 'history': task_history})


@login_required
def task_stats(request):
    tasks = Task.objects.filter(owner=request.user)
    active_tasks = tasks.filter(status='Active')
    completed_tasks = tasks.filter(status='Completed')
    total_tasks = tasks.count()
    completed_percentage = (completed_tasks.count() / total_tasks) * 100
    remaining_percentage = 100 - completed_percentage

    print('Active Tasks Count:', active_tasks.count()) 
    print('Completed Tasks Count:', completed_tasks.count()) 
    return render(request, 'task_stats.html', {
        'active_tasks': active_tasks,
        'completed_tasks': completed_tasks,
        'completed_percentage': completed_percentage,
        'remaining_percentage': remaining_percentage,
        'total_tasks': total_tasks,
    })


   