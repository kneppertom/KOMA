from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

# Beispiel: Berechtigung prüfen oder erstellen
content_type = ContentType.objects.get_for_model(User)

# Ticket-Berechtigung
ticket_permission, created = Permission.objects.get_or_create(
    codename='can_manage_tickets',
    defaults={'name': 'Kann Tickets verwalten', 'content_type': content_type},
)

# Statistik-Berechtigung
statistics_permission, created = Permission.objects.get_or_create(
    codename='can_view_statistics',
    defaults={'name': 'Kann Statistiken ansehen', 'content_type': content_type},
)

class Ticket(models.Model):
    STATUS_CHOICES = [
        ('Received', 'Eingegangen'),
        ('IN_PROGRESS', 'In Bearbeitung'),
        ('QUESTION_OPEN', 'Frage offen'),
        ('QUESTION_ANSWERED', "Frage beantwortet"),
        ('FORWARDED', 'Weitergeleitet'),
        ('CLOSED', 'Geschlossen'),
    ]

    CATEGORY_CHOICES = [
        ('TYPO', 'Tippfehler'),
        ('CONTENT', 'Inhaltliche Unstimmigkeit'),
        ('SUGGESTION', 'Verbesserungsvorschlag'),
        ('GENERAL', 'Allgemein')
    ]

    AFFECTED_MATERIALS_CHOICES = [
        ('SKRIPT', 'Skript'),
        ('TUTORIEN', 'Tutorien'),
        ('BOOKS', 'Bücher'),
        ('GENERAL', 'Allgemein')
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
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, verbose_name="Kategorie", null=True, blank=True)
    affected_materials = models.ManyToManyField('AffectedMaterial', verbose_name="Betroffene Materialien")
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='assigned_tickets')

    def __str__(self):
        return self.title

class AffectedMaterial(models.Model):
    name = models.CharField(max_length=20, choices=Ticket.AFFECTED_MATERIALS_CHOICES, unique=True)

    def __str__(self):
        return self.get_name_display()
class Meta:
    app_label = 'Koma'
    permissions = [
        ("can_view_tickets", "Can view tickets"),
        ("can_view_users", "Can view users"),
    ]

# TicketHistory Modell, ersetzt ChangeHistory
class TicketHistory(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, verbose_name="Ticket", related_name="history_entries")
    change_id = models.AutoField(primary_key=True)  # Automatische fortlaufende Nummer
    text = models.TextField(verbose_name="Text")  # Vom Benutzer hinzugefügter Text
    status = models.CharField(max_length=20, choices=Ticket.STATUS_CHOICES, verbose_name="Status")  # Referenzstatus
    datetime = models.DateTimeField(auto_now_add=True, verbose_name="Änderungsdatum")  # Datum und Uhrzeit des Eintrags
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Geändert von")  # Benutzer, der den Eintrag erstellt hat

    def __str__(self):
        return f"History #{self.change_id} für Ticket {self.ticket.title} - Status: {self.status}"

    class Meta:
        app_label = 'Koma'
        verbose_name_plural = "Ticket Histories"

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