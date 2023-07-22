from django.conf import settings
from django.db import models
from django.utils import timezone

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    due_date = models.DateTimeField(null=True, blank=True)
    PRIORITY_CHOICES = (
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    )
    priority = models.CharField(choices=PRIORITY_CHOICES, default='Low',max_length=20)
    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Completed', 'Completed'),
    )
    status = models.CharField(choices=STATUS_CHOICES, default='Active',max_length=20)

class TaskHistory(models.Model):
    ACTION_CHOICES = [
        ('created','Created'),
        ('updated','Updated'),

    ]
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    action = models.CharField(choices = ACTION_CHOICES,max_length=20)
    timestamp = models.DateTimeField(default=timezone.now) 

    def __str__(self):
        return f'{self.action} on task {self.task.title}'
    
    @classmethod
    def create(cls,task,action):
        task_history = cls(task = task , action = action)
        task_history.save()
        return task_history