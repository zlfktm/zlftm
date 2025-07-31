from django import forms
from todo.models import Todo, Comment


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ('title', 'description', 'start_date', 'end_date')

class TodoUpdateForm(forms.ModelForm):
    class Meta:
        model = Todo
        template_name = 'todo_update.html'
        fields = ('title', 'description', 'start_date', 'end_date', 'is_completed')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('message',)
        labels = {
            'message' : '내용'
        }
        widgets = {
            'message' : forms.Textarea(attrs={
                'rows' : '3',
                'cols' : '20',
                'class' : 'form-control',
                'placeholder' : '내용을 입력하세요.'
            })
        }
