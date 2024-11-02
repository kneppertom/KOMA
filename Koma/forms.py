from django import forms
from .models import Ticket, AffectedMaterial

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = [
            'title', 'description', 'priority', 'module', 'category', 'affected_materials'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Geben Sie den Titel ein'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Beschreibung'}),
            'priority': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Priorität'}),
            # 'status': forms.Select(attrs={'class': 'form-select'}),
            'module': forms.Select(attrs={'class': 'form-select'}),
            # 'assigned_to': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),  # Einzelauswahl
            'affected_materials': forms.CheckboxSelectMultiple()  # Mehrfachauswahl
        }

        # Optional: Custom initialization to set queryset for affected_materials
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['affected_materials'].queryset = AffectedMaterial.objects.all()

