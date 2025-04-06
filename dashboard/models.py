from django.db import models
import uuid

class ScriptInfo(models.Model):
    script_id = models.UUIDField(primary_key=True)  
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    upvotes = models.PositiveIntegerField(default=0)
    public = models.BooleanField(default=False)
    email = models.EmailField(default="" , blank=True) 
    text = models.TextField(default="", blank=True)


