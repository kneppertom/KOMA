from operator import truediv
from pickle import FALSE

from django.contrib.auth.models import Permission, User
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from .models import Ticket
from django.contrib.contenttypes.models import ContentType

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
def create_ticket(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        ticket = Ticket.objects.create(
            title=title,
            description=description,
            created_by=request.user
        )
        return redirect('ticket_list')  # Beispiel-Redirect, passe es an deine URLs an

    return render(request, 'tickets/create_ticket.html')

@login_required
# def user_list(request):
#     # Hole alle Benutzer und Berechtigungen
#     users = User.objects.all()
#
#     # Erstelle eine Liste von Benutzern und deren Berechtigungen
#     user_permissions = []
#     for user in users:
#         permissions = user.get_all_permissions()  # Hole alle Berechtigungen des Benutzers
#         user_permissions.append({
#             'user': user,
#             'permissions': permissions,
#         })
#
#     # Übergib die Liste an das Template
#     context = {'user_permissions': user_permissions}
#     return render(request, 'user-list/user_list.html', context)

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