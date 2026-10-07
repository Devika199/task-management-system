from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
class Registeration(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    name = models.CharField(max_length=100)
    address = models.TextField()
    phone = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)

class Task(models.Model):

    STATUS_CHOICES = [
        ('todo', 'Todo'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=200)

    description = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='todo'
    )

    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='medium'
    )

    due_date = models.DateField(null=True, blank=True)

    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title