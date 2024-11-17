from operator import truediv
from pickle import FALSE

from django.contrib.auth.models import Permission, User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from .models import Ticket, TicketHistory
from django.contrib.contenttypes.models import ContentType
from .forms import TicketForm, TicketHistoryForm
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Account created for {user.username}!')
            login(request, user)  # Benutzer direkt nach der Registrierung einloggen
            return redirect('home')  # Weiterleitung zur Home-Seite nach der Registrierung
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def home(request):
    user = request.user
    has_ticket_permission = user.has_perm('Ticketsystem.view_ticket')
    has_userview_permission = user.has_perm('Ticketsystem.view_ticket')
    context = {'has_ticket_permission': has_ticket_permission, 'has_userview_permission': has_userview_permission}
    print(f"has_settings_permission: {has_userview_permission}")  # Debug-Ausgabe
    return render(request, 'home.html', context)

def ticket_list(request):
    tickets = Ticket.objects.all()  # Hier werden alle Tickets abgerufen
    return render(request, 'tickets/ticket_overview.html', {'tickets': tickets})

@login_required
#@permission_required('Ticketsystem.change_settings', raise_exception=True)
def user_list(request):
    users = User.objects.all()
    all_permissions = Permission.objects.all()

    # Wenn das Formular gesendet wird
    if request.method == 'POST' and 'save_user' in request.POST:
        user_id = request.POST.get('save_user')
        user = User.objects.get(id=user_id)

        # Hole die ausgewählten Berechtigungen
        permission_ids = request.POST.getlist(f'permissions_{user_id}')
        new_permissions = Permission.objects.filter(id__in=permission_ids)

        # Setze neue Berechtigungen für den Benutzer
        user.user_permissions.set(new_permissions)
        user.save()

        # Leite nach dem Speichern weiter (optional)
        return redirect('user_list')

    # Erstelle eine Liste von Benutzern und deren Berechtigungen
    user_permissions = []
    for user in users:
        permissions = user.get_all_permissions()
        user_permissions.append({
            'user': user,
            'permissions': permissions,
        })

    # Übergib alle Berechtigungen und Benutzerdaten an das Template
    context = {
        'user_permissions': user_permissions,
        'all_permissions': all_permissions
    }
    return render(request, 'user-list/user_list.html', context)

from .forms import TicketForm

@login_required
def ticket_overview(request, ticket_id=None):
    tickets = Ticket.objects.all().order_by('-created_at')
    selected_ticket = get_object_or_404(Ticket, id=ticket_id) if ticket_id else tickets.first()

    history_entries = TicketHistory.objects.filter(ticket=selected_ticket).order_by('-datetime') if selected_ticket else []

    context = {
        'tickets': tickets,
        'selected_ticket': selected_ticket,
        'history_entries': history_entries,
        'form': TicketForm(instance=selected_ticket),
    }
    return render(request, 'tickets/ticket_overview.html', context)

def get_ticket(request, ticket_id):
    try:
        ticket = Ticket.objects.get(id=ticket_id)
        history = TicketHistory.objects.filter(ticket=ticket).order_by('-datetime')
        affected_materials = list(ticket.affected_materials.all().values_list('name', flat=True))

        history_data = [
            {
                'datetime': entry.datetime.strftime('%Y-%m-%d %H:%M:%S'),
                'user': entry.user.username,
                'text': entry.text,
                'status': entry.status,
            }
            for entry in history
        ]

        data = {
            'id': ticket.id,
            'title': ticket.title,
            'priority': ticket.priority,
            'status': ticket.status,
            'module': ticket.module.name if ticket.module else None,
            'category': ticket.category if ticket.category else None,
            'affected_materials': affected_materials,
            'description': ticket.description,
            'created_at': ticket.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'history': history_data,
        }
        return JsonResponse(data)
    except Ticket.DoesNotExist:
        return JsonResponse({'error': 'Ticket not found'}, status=404)

def edit_ticket(request, ticket_id):
    # ticket = get_object_or_404(Ticket, id=ticket_id)
    ticket = Ticket.objects.get(id=ticket_id)
    if request.method == 'POST':
        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            messages.success(request, "Das Ticket wurde erfolgreich aktualisiert.")
            return JsonResponse({'status': 'success', 'message': 'Ticket aktualisiert'})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    else:
        # JSON-Daten für das Ticket zurückgeben, wenn GET-Request
        data = {
            'id': ticket.id,
            'title': ticket.title,
            'description': ticket.description,
            'priority': ticket.priority,
            'module': ticket.module.id if ticket.module else None,
            'category': ticket.category if ticket.category else None,
            'affected_materials': list(ticket.affected_materials.values_list('id', flat=True)),
        }
        return JsonResponse(data)

# # View zum Erstellen eines neuen Tickets
# def create_ticket(request):
#     if request.method == 'POST':
#         form = TicketForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect(reverse('ticket_list'))  # Zurück zur Ticketliste oder zu einer anderen Zielseite
#     else:
#         form = TicketForm()
#
#     return render(request, 'tickets/ticket_form.html', {'form': form, 'action': 'Erstellen'})

# View zum Erstellen eines neuen Tickets
def create_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.created_by = request.user
            ticket = form.save()
            # Wenn der Request über AJAX kommt, JSON-Antwort zurückgeben
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success', 'ticket_id': ticket.id})
            # Ansonsten eine reguläre Umleitung
            return redirect(reverse('ticket_list'))  # Zielseite bei erfolgreicher Speicherung
        else:
            # Bei Validierungsfehlern auch JSON zurückgeben
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    else:
        form = TicketForm()

    # Für reguläre, nicht-JavaScript-basierte Aufrufe
    return render(request, 'tickets/ticket_form.html', {'form': form, 'action': 'Erstellen'})

def update_ticket(request, ticket_id):
    # Ticket-Objekt aus der Datenbank holen
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if request.method == "POST":
        # Das Formular mit POST-Daten und dem bestehenden Ticket-Objekt füllen
        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            # Wenn das Formular gültig ist, Ticket speichern
            form.save()
            # Wenn der Request über AJAX kommt, eine JSON-Antwort senden
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success', 'message': 'Ticket erfolgreich aktualisiert'})

            # Ansonsten eine reguläre Umleitung oder das Rendern einer HTML-Seite
            return redirect(reverse('ticket_overview', kwargs={'ticket_id': ticket.id}))

    else:
        # Wenn es kein POST-Request ist, wird das Formular zum Bearbeiten angezeigt
        form = TicketForm(instance=ticket)

    # Formular-Template nur bei GET-Anfragen laden
    return render(request, 'tickets/ticket_overview.html', {'form': form})

@login_required
def add_remark(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if request.method == 'POST':
        form = TicketHistoryForm(request.POST)
        if form.is_valid():
            remark = form.save(commit=False)
            remark.ticket = ticket
            remark.user = request.user  # Angemeldeter Benutzer wird als User gesetzt
            remark.save()
            # Erfolgreiche JSON-Antwort
            return JsonResponse({'status': 'success', 'message': 'Bemerkung hinzugefügt'})
        else:
            # Fehlerhafte JSON-Antwort mit Formularfehlern
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)

    # Falls eine GET-Anfrage auf diese View geschickt wird, schicke eine leere JSON-Antwort oder eine Fehlermeldung
    return JsonResponse({'status': 'error', 'message': 'GET-Anfrage nicht erlaubt'}, status=405)

@login_required
def statistic_overview(request):
    # Daten für das Ticketstatus-Diagramm abrufen
    status_counts = {
        'Eingegangen': Ticket.objects.filter(status='Received').count(),
        'In Bearbeitung': Ticket.objects.filter(status='IN_PROGRESS').count(),
        'Frage offen': Ticket.objects.filter(status='QUESTION_OPEN').count(),
        'Frage beantwortet': Ticket.objects.filter(status='QUESTION_ANSWERED').count(),
        'Weitergeleitet': Ticket.objects.filter(status='FORWARDED').count(),
        'Geschlossen': Ticket.objects.filter(status='CLOSED').count(),
    }

    # Daten für das Ticketkategorien-Diagramm abrufen
    category_counts = {
        'Tippfehler': Ticket.objects.filter(category='TYPO').count(),
        'Inhaltliche Unstimmigkeit': Ticket.objects.filter(category='CONTENT').count(),
        'Verbesserungsvorschlag': Ticket.objects.filter(category='SUGGESTION').count(),
        'Allgemein': Ticket.objects.filter(category='GENERAL').count(),
    }

    # Kontext mit Daten für die Diagramme erstellen
    context = {
        'status_counts': status_counts,
        'category_counts': category_counts,
    }

    return render(request, 'statistics/statistic_overview.html', context)
