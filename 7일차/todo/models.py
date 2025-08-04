from io import BytesIO
from pathlib import Path

from PIL import Image
from django.contrib.auth.models import User
from django.db import models

class Todo(models.Model):
    title = models.CharField('제목',max_length=50)
    description = models.TextField('설명')
    start_date = models.DateField('시작일')
    end_date = models.DateField('마감일')
    is_completed = models.BooleanField('완료 여부',default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    completed_image = models.ImageField('완료 이미지', null=True, blank=True, upload_to='image/completed')
    thumbnail = models.ImageField('썸네일', null=True, blank=True, upload_to='image/completed/thumbnail', default='image/completed_default.png')

    created_at = models.DateTimeField('생성 시간',auto_now_add=True)
    updated_at = models.DateTimeField('수정 시간',auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.completed_image :
            return super().save(*args, **kwargs)

        image = Image.open(self.completed_image)
        image.thumbnail((300, 300))

        image_path = Path(self.completed_image.name)

        thumbnail_name = image_path.stem    # blog/2025-07-41/database.png => database만 가져옴
        thumbnail_extension = image_path.suffix.lower() # blog/2025-07-41/database.png => .png만 가져옴
        thumbnail_filename = f"{thumbnail_name}_thumb{thumbnail_extension}" # databse_thumb.png

        if thumbnail_extension in ['.jpg', '.jpeg'] :
            file_type = 'JPEG'
        elif thumbnail_extension == '.gif' :
            file_type = 'GIF'
        elif thumbnail_extension == '.png' :
            file_type = 'PNG'
        else :
            return super().save(*args, **kwargs)

        temp_thumb = BytesIO()
        image.save(temp_thumb, file_type)
        temp_thumb.seek(0)

        self.thumbnail.save(thumbnail_filename, temp_thumb, save=False)
        temp_thumb.close()
        return super().save(*args, **kwargs)


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