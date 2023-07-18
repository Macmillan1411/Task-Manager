from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('title', 'description', 'priority', 'status', 'due_date')
        widgets = {
            'due_date': forms.DateTimeInput(attrs={'class': 'datetime-input'}),
        }