from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('title', 'description', 'priority', 'status', 'due_date')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Task Title'}),
            'description': forms.Textarea(attrs={'class': 'textarea', 'placeholder': 'Task Description'}),
            'priority': forms.Select(attrs={'class': 'select'}),
            'status': forms.Select(attrs={'class': 'select'}),
            'due_date': forms.TextInput(attrs={'class': 'input datetime-input', 'placeholder': 'Due Date'}),
        }
