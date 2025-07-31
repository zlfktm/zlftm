from urllib import request

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.urls.base import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.http.response import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404

from todo.models import Todo, Comment
from todo.forms import CommentForm


class TodoListView(LoginRequiredMixin, ListView):
    model = Todo
    template_name = 'todo_list.html'
    paginate_by = 10
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()

        if not self.request.user.is_superuser :
            queryset = queryset.filter(author=self.request.user)

        q = self.request.GET.get('q')

        if q :
            from django.db.models.query_utils import Q
            queryset = queryset.filter(
                Q(title__icontains=q) |
                Q(description__icontains=q)
            )

        return queryset


class TodoDetailView(LoginRequiredMixin, DetailView):
    model = Todo
    template_name = 'todo_info.html'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.author != self.request.user and not self.request.user.is_superuser :
            raise Http404
        return self.object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dict'] = self.object.__dict__
        context['comment_form'] = CommentForm()

        # comment pagination
        comment = self.object.comments.all().select_related('user')
        paginator = Paginator(comment, 5)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['page_obj'] = page_obj
        return context


class TodoCreateView(LoginRequiredMixin, CreateView):
    model = Todo
    template_name = 'todo_create.html'
    fields = ['title', 'description', 'start_date', 'end_date']

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('cbv_todo_list')


class TodoUpdateView(LoginRequiredMixin, UpdateView):
    model = Todo
    template_name = 'todo_update.html'
    fields = ['title', 'description', 'start_date', 'end_date', 'is_completed']

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.author != self.request.user and not self.request.user.is_superuser :
            raise Http404
        return self.object

    def get_success_url(self):
        return reverse_lazy('cbv_todo_info', kwargs={'pk': self.object.pk})


class TodoDeleteView(LoginRequiredMixin, DeleteView):
    model = Todo

    def get(self, *args, **kwargs) :
        raise Http404

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.author != self.request.user and not self.request.user.is_superuser :
            raise Http404
        return self.object

    def get_success_url(self):
        return reverse_lazy('cbv_todo_list')


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    pk_url_kwarg = 'todo_id'

    def get(self, *args, **kwargs) :
        raise Http404

    def form_valid(self, form):
        todo = get_object_or_404(Todo, pk=self.kwargs['todo_id'])
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.todo = todo
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        base_url = reverse_lazy('cbv_todo_info', kwargs={'pk': self.object.todo.pk})
        return f"{base_url}#comment_wrapper"


class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'comment_update.html'

    def get_success_url(self):
        page = self.request.GET.get('page', '1')
        base_url = reverse_lazy('cbv_todo_info', kwargs={'pk': self.object.todo.pk})
        return f"{base_url}?page={page}#comment_wrapper"


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment

    def get(self, *args, **kwargs) :
        raise Http404

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.user != self.request.user and not self.request.user.is_superuser :
            raise Http404
        return self.object

    def get_success_url(self):
        page = self.request.GET.get('page', '1')
        base_url = reverse_lazy('cbv_todo_info', kwargs={'pk': self.object.todo.pk})
        return f"{base_url}?page={page}#comment_wrapper"
