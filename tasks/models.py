from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    due_date = models.DateTimeField(null=True, blank=True)
    PRIORITY_CHOICES = (
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    )
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='Low')
    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Completed', 'Completed'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')

class TaskHistory(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    due_date = models.DateTimeField(null=True, blank=True)
    PRIORITY_CHOICES = (
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    )
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='Low')
    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Completed', 'Completed'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    @classmethod
    def create(cls, task):
        return cls(
            task=task,
            title=task.title,
            description=task.description,
            completed=task.completed,
            due_date=task.due_date,
            priority=task.priority,
            status=task.status
        )

@receiver(post_save, sender=Task)
def create_task_history(sender, instance, created, **kwargs):
    if not created and instance.owner == instance.updated_by:
        previous_instance = sender.objects.get(pk=instance.pk)
        changes = {}
        for field in sender._meta.fields:
            field_name = field.name
            if getattr(instance, field_name) != getattr(previous_instance, field_name):
                changes[field_name] = (getattr(previous_instance, field_name), getattr(instance, field_name))
        if changes:
            TaskHistory.objects.create(
                task=instance,
                title=changes.get('title', ('', ''))[0],
                description=changes.get('description', ('', ''))[0],
                completed=changes.get('completed', (False, False))[0],
                due_date=changes.get('due_date', (None, None))[0],
                priority=changes.get('priority', ('', ''))[0],
                status=changes.get('status', ('', ''))[0],
                updated_by=instance.owner
            )