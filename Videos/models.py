from django.db import models
import datetime
from django.utils.translation import gettext as _

class CategoryItem(models.Model):
    name = models.CharField(_("Category Name"),max_length=100)
    created_at = models.DateField(_("Created At"), default=datetime.date.today)
    def __str__(self):
        return f'{self.name} {self.name}'
    
class VideoItem(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(_('Description'), max_length=None)
    category = models.ForeignKey(
            CategoryItem,
            related_name='Category',
            on_delete=models.CASCADE,
            default=None
    )
    author = models.CharField(max_length=100)
    created_at = models.DateField(_("Created At"), default=datetime.date.today)
    video_file = models.FileField(upload_to='videos', blank=True, null=True)
    video_file_480p = models.FileField(upload_to='videos', blank=True, null=True)
    video_file_720p = models.FileField(upload_to='videos', blank=True, null=True)
    video_file_1080p = models.FileField(upload_to='videos', blank=True, null=True)
    def __str__(self):
        return f'{self.id}. |  {self.title}  |  {self.category.name} '
