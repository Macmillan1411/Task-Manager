from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Task, TaskHistory
from .forms import TaskForm
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import Signal

from django.urls import reverse, resolve
from . import views

class TaskViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.task = Task.objects.create(title='Test Task', owner=self.user)

    def test_task_list_view(self):
        response = self.client.get(reverse('tasks:task_list'))
        self.assertEqual(response.status_code, 200)
        # Add more assertions to check if the correct template and data are rendered

    def test_task_detail_view(self):
        response = self.client.get(reverse('tasks:task_detail', args=[self.task.pk]))
        self.assertEqual(response.status_code, 200)
        # Add more assertions to check if the correct template and data are rendered

    def test_task_new_view(self):
        response = self.client.post(reverse('tasks:task_new'), {'title': 'New Task'})
        self.assertEqual(response.status_code, 302)  # 302 is the redirect status code after creating a new task
        self.assertTrue(Task.objects.filter(title='New Task').exists())
        # Add more assertions to check if the new task is created correctly

    def test_task_edit_view(self):
        response = self.client.post(reverse('tasks:task_edit', args=[self.task.pk]), {'title': 'Updated Task'})
        self.assertEqual(response.status_code, 302)  # 302 is the redirect status code after updating a task
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Updated Task')
        # Add more assertions to check if the task is updated correctly

    def test_task_delete_view(self):
        response = self.client.post(reverse('tasks:task_delete', args=[self.task.pk]))
        self.assertEqual(response.status_code, 302)  # 302 is the redirect status code after deleting a task
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())
        # Add more assertions to check if the task is deleted correctly

    def test_task_history_view(self):
        TaskHistory.objects.create(task=self.task, action='created')
        response = self.client.get(reverse('tasks:task_history', args=[self.task.pk]))
        self.assertEqual(response.status_code, 200)
        # Add more assertions to check if the correct template and data are rendered

    def test_task_stats_view(self):
        response = self.client.get(reverse('tasks:task_stats'))
        self.assertEqual(response.status_code, 200)
        # Add more assertions to check if the correct template and data are rendered



class TaskModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.task = Task.objects.create(
            title='Test Task',
            description='This is a test task',
            owner=self.user,
            due_date=timezone.now() + timezone.timedelta(days=1),
            priority='Medium',
            status='Active'
        )

    def test_task_creation(self):
        self.assertEqual(self.task.title, 'Test Task')
        self.assertEqual(self.task.description, 'This is a test task')
        self.assertEqual(self.task.owner, self.user)
        self.assertIsNotNone(self.task.created_at)
        self.assertIsNotNone(self.task.updated_at)
        self.assertIsNotNone(self.task.due_date)
        self.assertEqual(self.task.priority, 'Medium')
        self.assertEqual(self.task.status, 'Active')

class TaskHistoryModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.task = Task.objects.create(
            title='Test Task',
            description='This is a test task',
            owner=self.user,
            due_date=timezone.now() + timezone.timedelta(days=1),
            priority='Medium',
            status='Active'
        )

    def test_task_history_creation(self):
        task_history = TaskHistory.objects.create(task=self.task, action='created')
        self.assertEqual(task_history.task, self.task)
        self.assertEqual(task_history.action, 'created')
        self.assertIsNotNone(task_history.timestamp)


User = get_user_model()

class SignalTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_create_task_history_signal(self):
        # Create a new Task instance
        task = Task.objects.create(
            title='Test Task',
            description='This is a test task',
            owner=self.user,
            priority='Medium',
            status='Active'
        )

        # Check if the TaskHistory instance is created with action='created'
        task_history = TaskHistory.objects.get(task=task, action='created')
        self.assertIsNotNone(task_history)
        self.assertEqual(task_history.task, task)
        self.assertEqual(task_history.action, 'created')

    def test_update_task_history_signal(self):
        # Create a new Task instance
        task = Task.objects.create(
            title='Test Task',
            description='This is a test task',
            owner=self.user,
            priority='Medium',
            status='Active'
        )

        # Modify the Task instance
        task.title = 'Updated Test Task'
        task.save()

        # Check if the TaskHistory instance is created with action='updated'
        task_history = TaskHistory.objects.get(task=task, action='updated')
        self.assertIsNotNone(task_history)
        self.assertEqual(task_history.task, task)
        self.assertEqual(task_history.action, 'updated')

    def test_create_task_history_signal_existing_instance(self):
        # Create a new Task instance
        task = Task.objects.create(
            title='Test Task',
            description='This is a test task',
            owner=self.user,
            priority='Medium',
            status='Active'
        )

        # Create a TaskHistory instance manually with action='created'
        task_history = TaskHistory.objects.create(task=task, action='created')

        # Save the Task instance again to trigger the update action
        task.save()

        # Check if the TaskHistory instance with action='created' still exists and no new instance is created
        self.assertTrue(TaskHistory.objects.filter(task=task, action='created').exists())
        self.assertFalse(TaskHistory.objects.filter(task=task, action='updated').exists())



class UrlsTests(TestCase):
    def test_task_list_url(self):
        url = reverse('tasks:task_list')
        self.assertEqual(resolve(url).func, views.task_list)

    def test_task_detail_url(self):
        task_id = 1  # Replace 1 with a valid task ID for testing
        url = reverse('tasks:task_detail', args=[task_id])
        self.assertEqual(resolve(url).func, views.task_detail)

    def test_task_new_url(self):
        url = reverse('tasks:task_new')
        self.assertEqual(resolve(url).func, views.task_new)

    def test_task_edit_url(self):
        task_id = 1  # Replace 1 with a valid task ID for testing
        url = reverse('tasks:task_edit', args=[task_id])
        self.assertEqual(resolve(url).func, views.task_edit)

    def test_task_delete_url(self):
        task_id = 1  # Replace 1 with a valid task ID for testing
        url = reverse('tasks:task_delete', args=[task_id])
        self.assertEqual(resolve(url).func, views.task_delete)

    def test_task_history_url(self):
        task_id = 1  # Replace 1 with a valid task ID for testing
        url = reverse('tasks:task_history', args=[task_id])
        self.assertEqual(resolve(url).func, views.task_history)

    def test_task_stats_url(self):
        url = reverse('tasks:task_stats')
        self.assertEqual(resolve(url).func, views.task_stats)
