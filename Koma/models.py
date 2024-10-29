from django.db import models
from django.contrib.auth.models import User

class Ticket(models.Model):
    STATUS_CHOICES = [
        ('Received', 'Eingegangen'),
        ('IN_PROGRESS', 'In Bearbeitung'),
        ('QUESTION_OPEN', 'Frage offen'),
        ('QUESTION_ANSWERED', "Frage beantwortet"),
        ('FORWARDED', 'Weitergeleitet'),
        ('CLOSED', 'Geschlossen'),
    ]

    # Ticket Modell Attribute
    title = models.CharField(max_length=200, verbose_name="Titel")
    description = models.TextField(verbose_name="Beschreibung")
    priority = models.IntegerField(verbose_name="Priorität")  # Das ist neu hinzugefügt
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Received', verbose_name="Status")
    module = models.ForeignKey('Module', on_delete=models.SET_NULL, null=True, verbose_name="Modul")  # ForeignKey zu Module
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tickets', verbose_name="Erstellt von")
    inspector = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='inspected_tickets', verbose_name="Prüfer")  # Inspektor/Prüfer
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Erstellt am")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Aktualisiert am")

    def __str__(self):
        return self.title

    class Meta:
        app_label = 'Koma'
        permissions = [
            ("can_view_tickets", "Can view tickets"),
            ("can_view_users", "Can view users"),
        ]

# ChangeHistory Modell
class ChangeHistory(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, verbose_name="Ticket", related_name="changes")
    text_old = models.TextField(verbose_name="Alter Text", null=True, blank=True)
    text_new = models.TextField(verbose_name="Neuer Text", null=True, blank=True)
    state_old = models.CharField(max_length=20, choices=Ticket.STATUS_CHOICES, verbose_name="Alter Status", null=True, blank=True)
    state_new = models.CharField(max_length=20, choices=Ticket.STATUS_CHOICES, verbose_name="Neuer Status", null=True, blank=True)
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Geändert von")
    change_date = models.DateTimeField(auto_now_add=True, verbose_name="Änderungsdatum")

    def __str__(self):
        return f"Änderung für {self.ticket.title} am {self.change_date}"

    class Meta:
        app_label = 'Koma'

# Module Modell
class Module(models.Model):
    name = models.CharField(max_length=100, verbose_name="Modulname")
    short_name = models.CharField(max_length=20, verbose_name="Kurzname")

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'Koma'


# ModuleManager Modell
class ModuleManager(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, verbose_name="Modul")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Benutzer")

    def __str__(self):
        return f"{self.user.username} verwaltet {self.module.name}"

    class Meta:
        app_label = 'Koma'
        unique_together = ('module', 'user')

# Erweiterung des User-Modells
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Benutzer")
    service_level = models.CharField(max_length=50, verbose_name="Service Level")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Erstellt am")
    last_login = models.DateTimeField(null=True, blank=True, verbose_name="Letzter Login")

    def __str__(self):
        return self.user.username

    class Meta:
        app_label = 'Koma'


# Login Modell (falls es benötigt wird)
class Login(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Benutzer")
    username = models.CharField(max_length=25, unique=True, verbose_name="Benutzername")
    password = models.CharField(max_length=128, verbose_name="Passwort")

    def __str__(self):
        return self.username

    class Meta:
        app_label = 'Koma'