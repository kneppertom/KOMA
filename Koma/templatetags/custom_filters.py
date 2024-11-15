# custom_filters.py
from django import template

register = template.Library()

@register.filter
def matches_suffix(value, arg):
    # Prüft, ob ein Element in value den Suffix (Teil nach dem '.') von arg enthält.
    # Falls value leer oder None ist, sofort False zurückgeben
    if not value:
        return False

    if value and arg:
        suffix = arg.split('.')[-1]  # Extrahiere den Teil nach dem Punkt
        print(f"Vergleich mit Suffix: {suffix}")

        # Falls value eine Liste oder Menge ist
        if isinstance(value, (list, set)):
            return any(item.split('.')[-1] == suffix for item in
                       value)  # Überprüft, ob der Suffix enthalten ist

        # Falls value ein String ist
        return value.split('.')[-1] == suffix  # Prüft, ob value selbst diesen Suffix hat

    return False