from django.db import models

from users.models import CustomUser


"""class Post(models.Model):
    content = models.CharField(max_length=300)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='post-author')
    created_at = models.DateTimeField(auto_now_add=True)
    group = models.ForeignKey
    is_edited = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
"""

