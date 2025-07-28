from django.db import models
import uuid
from django_extensions.db.fields import AutoSlugField

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    
class Blog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='name', unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='blogs', null=True, blank=True)
    description = models.TextField()
    
    def __str__(self):
        return self.name
