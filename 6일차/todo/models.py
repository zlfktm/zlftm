from django.contrib.auth.models import User
from django.db import models

class Todo(models.Model):
    title = models.CharField('제목',max_length=50)
    description = models.TextField('설명')
    start_date = models.DateField('시작일')
    end_date = models.DateField('마감일')
    is_completed = models.BooleanField('완료 여부',default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField('생성 시간',auto_now_add=True)
    updated_at = models.DateTimeField('수정 시간',auto_now=True)

    def __str__(self):
        return self.title

    class Meta :
        verbose_name = 'Todo'
        verbose_name_plural = 'Todo 목록'


class Comment(models.Model) :
    todo = models.ForeignKey(Todo, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    message = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.todo.title} 댓글'

    class Meta:
        verbose_name = '댓글'
        verbose_name_plural = '댓글 목록'
        ordering = ['-created_at', 'id']