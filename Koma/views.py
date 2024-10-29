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
from .forms import TicketForm
from django.shortcuts import render, get_object_or_404, redirect

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

# Prüfer kann Tickets bearbeiten und schließen
@permission_required('Ticketsystem.change_ticket', raise_exception=True)
def edit_ticket(request, ticket_id):
    # Logik zum Bearbeiten eines Tickets
    pass

@permission_required('Ticketsystem.close_ticket', raise_exception=True)
def close_ticket(request, ticket_id):
    # Logik zum Schließen eines Tickets
    pass


@login_required
def ticket_form(request, ticket_id=None):
    return render(request, 'tickets/create/ticket_form.html')
    ticket = None
    if ticket_id:
        ticket = get_object_or_404(Ticket, id=ticket_id)

    if request.method == 'POST':
        if ticket:
            form = TicketForm(request.POST, instance=ticket)
        else:
            form = TicketForm(request.POST)

        if form.is_valid():
            ticket = form.save(commit=False)
            if not ticket_id:  # Falls es ein neues Ticket ist, setzen wir den Ersteller
                ticket.created_by = request.user
            ticket.save()
            messages.success(request, "Das Ticket wurde erfolgreich gespeichert.")
            return redirect('ticket_list')
    else:
        form = TicketForm(instance=ticket)

    return render(request, 'ticket_form.html', {
        'form': form,
        'ticket': ticket,
        'status_choices': Ticket.STATUS_CHOICES if ticket else None
    })

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
def ticket_overview(request):
    tickets = Ticket.objects.all().order_by('-created_at')
    selected_ticket = tickets.first() if tickets.exists() else None
    history_entries = []  # Standardmäßig leere Liste für den Verlauf

    # Historie des ausgewählten Tickets abrufen, falls ein Ticket ausgewählt ist
    if selected_ticket:
        history_entries = TicketHistory.objects.filter(ticket=selected_ticket).order_by('-datetime')

    # Formularverarbeitung für ein neues Ticket
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            new_ticket = form.save(commit=False)
            new_ticket.assigned_to = request.user
            new_ticket.created_by = request.user
            new_ticket.save()
            # TicketHistory-Eintrag erstellen, wenn ein neues Ticket angelegt wird
            TicketHistory.objects.create(
                ticket=new_ticket,
                text="Ticket erstellt",
                status=new_ticket.status,
                datetime=new_ticket.created_at,
                user=request.user
            )
            return redirect('ticket_overview')
    else:
        form = TicketForm()

    context = {
        'tickets': tickets,
        'selected_ticket': selected_ticket,
        'history_entries': history_entries,  # Historie dem Kontext hinzufügen
        'form': form,  # Das Formular für ein neues Ticket
    }
    return render(request, 'tickets/ticket_overview.html', context)


def get_ticket(request, ticket_id):
    try:
        ticket = Ticket.objects.get(id=ticket_id)
        history = TicketHistory.objects.filter(ticket=ticket).order_by('-datetime')

        # Erstelle JSON-kompatibles Format für die Historie
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
            'inspector': ticket.inspector.username if ticket.inspector else '',
            'description': ticket.description,
            'created_at': ticket.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'history': history_data,
        }
        return JsonResponse(data)
    except Ticket.DoesNotExist:
        return JsonResponse({'error': 'Ticket not found'}, status=404)