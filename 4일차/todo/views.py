from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models.query_utils import Q
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.decorators.http import require_http_methods

from todo.forms import TodoForm, TodoUpdateForm
from todo.models import Todo


@login_required
def todo_list(request):
    todos = Todo.objects.filter(author=request.user).order_by('-created_at')

    q = request.GET.get('q')
    if q :
        todos = todos.filter(
            Q(title__icontains=q) |
            Q(description__icontains=q)
        )

    paginator = Paginator(todos, 7)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)

    context = {
        # 'todos': todos,
        'page_obj': page_obj,
    }

    return render(request, template_name='todo_list.html', context=context)


def todo_info(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id)
    context = {'todo' : todo}
    return render(request, template_name='todo_info.html', context=context)


@login_required
def todo_create(request) :
    form = TodoForm(request.POST or None)
    if form.is_valid():
        todo = form.save(commit=False)
        todo.author = request.user
        todo.save()
        return redirect(reverse('todo_info', kwargs={'todo_id' : todo.id}))

    context = {'form': form}
    return render(request, template_name='todo_create.html', context=context)


@login_required
def todo_update(request, todo_id) :
    todo = get_object_or_404(Todo, pk=todo_id, author=request.user)

    form = TodoUpdateForm(request.POST or None, instance=todo)
    if form.is_valid() :
        todo = form.save()
        return redirect(reverse('todo_info', kwargs={'todo_id' : todo.id}))

    context = {
        'todo' : todo,
        'form': form
    }

    return render(request, template_name='todo_update.html', context=context)


@login_required
@require_http_methods(['POST'])
def todo_delete(request, todo_id) :
    todo = get_object_or_404(Todo, pk=todo_id, author=request.user)
    todo.delete()

    return redirect(reverse('todo_list'))