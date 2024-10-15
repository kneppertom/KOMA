from django.db import models
from django.contrib.auth.models import User

class Ticket(models.Model):
    STATUS_CHOICES = [
        ('OPEN', 'Offen'),
        ('IN_PROGRESS', 'In Bearbeitung'),
        ('CLOSED', 'Geschlossen'),
    ]

    title = models.CharField(max_length=200, verbose_name="Titel")
    description = models.TextField(verbose_name="Beschreibung")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='OPEN', verbose_name="Status")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tickets', verbose_name="Erstellt von")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Erstellt am")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Aktualisiert am")

    def __str__(self):
        return self.title

    class Meta:
        app_label = 'Ticketsystem'
        permissions =[
             ("can_view_tickets", "Can view tickets"),
             ("can_view_users", "Can view users")
         ]