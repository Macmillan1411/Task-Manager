from django.db.models.signals import post_save
from django.dispatch import receiver 
from django.contrib.auth import get_user_model
from .models import Task,TaskHistory

User =  get_user_model()

@receiver(post_save, sender = Task)
def create_task_history(sender, instance, created, **kwargs):
    if created:
        action = 'created'
    else:
        action = 'updated'

   

    if not TaskHistory.objects.filter(task=instance,action = action).exists():
         TaskHistory.objects.create(task=instance,action=action)
