from django import forms
from .models import Ticket

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'priority', 'status', 'module', 'inspector']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Geben Sie den Titel ein'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Beschreibung'}),
            'priority': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Priorität'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'module': forms.Select(attrs={'class': 'form-select'}),
            'assigned_to': forms.Select(attrs={'class': 'form-select'}),
        }