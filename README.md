# Installationsanleitung für den Prototypen: "KOMA"

Diese Anleitung beschreibt die Installation und Inbetriebnahme des Prototyps "KOMA", der mit Python, Django und Bootstrap in der IDE PyCharm entwickelt wurde.

---

## Voraussetzungen

### 1. PyCharm Professional installieren
- Laden Sie **PyCharm Professional** von [diesem Link](https://www.jetbrains.com/de-de/pycharm) herunter.
- Installieren Sie PyCharm und aktivieren Sie die **Studentenlizenz**.
- Während der Installation setzen Sie bei "Create Associations" den Haken bei **".py"**, um Python-Dateien automatisch mit PyCharm zu verknüpfen.

### 2. GitHub Desktop installieren
- Laden Sie **GitHub Desktop** von [diesem Link](https://desktop.github.com/) herunter und installieren Sie es.
- Geben Sie Ihren **GitHub-Nutzernamen** an den Projektinhaber weiter, damit Sie zum Projekt hinzugefügt werden.

### 3. Python 3.12 installieren
- Laden Sie **Python 3.12** über den **Microsoft Store** herunter und installieren Sie es.

---

## Inbetriebnahme

### 1. GitHub Desktop starten
- Starten Sie **GitHub Desktop** und wählen Sie das Projekt **"kneppertom/KOMA"** aus.
- Klonen Sie das Projekt.

### 2. PyCharm starten und Projekt öffnen
- Öffnen Sie **PyCharm**.
- Öffnen Sie das geklonte Projekt, indem Sie den Ordner **"KOMA"** auswählen.
- Falls gefragt, **vertrauen Sie dem Projekt/dem übergeordneten Ordner**.

### 3. Befehle in der Konsole ausführen
- Öffnen Sie die Konsole **`>_`** in PyCharm und führen Sie die folgenden Befehle aus:

**Information**: In manchen Fällen kann es Vorkommen das der Befehl „**python**“ nicht funktioniert, hier kann als Alternative „**py**“ verwendet werden.

1. **Pip installieren/upgraden**:
	```python -m ensurepip --upgrade```
	
Dieser Befehl stellt sicher, dass pip (Python-Paketmanager) installiert oder aktualisiert wird, wodurch die Installation von Python-Paketen ermöglicht wird.

2. **Pip-Datei ausführen**:
```python get-pip.py```
	
Dies installiert pip, falls es noch nicht vorhanden ist, und ermöglicht die Verwaltung und Installation von Python-Paketen.

3. **Django-Framework installieren**:
```python -m pip install Django```

Dieser Befehl installiert das Django-Framework, das für die Entwicklung und den Betrieb des Projekts erforderlich ist.

4. **Django-Bootstrap v5 installieren**:
	```python -m pip install django-bootstrap-v5```
	
Dieses Paket integriert Bootstrap 5 in das Django-Projekt und ermöglicht die Verwendung moderner und responsiver Komponenten sowie Designs, die mit Bootstrap erstellt wurden.

5. **Django Widget Tweaks installieren**:
	```python -m pip install django-widget-tweaks```
	
Mit diesem Paket können Sie HTML-Formulare und Widgets in Ihrem Django-Projekt flexibel anpassen und erweitern. Es erleichtert die Anpassung von Formularelementen und das Hinzufügen von CSS-Klassen oder Attributen.

#### 3.1 Datenbankmigrationen ausführen
1. **Migrationsskript erstellen**:
	```python manage.py makemigrations```
	
Dieser Befehl erstellt neue Migrationsskripte basierend auf Änderungen an den Modellen. Falls keine Änderungen vorgenommen wurden, erscheint die Meldung "No changes detected".

2. **Migrationen anwenden**:
	```python manage.py migrate```
	
Dieser Befehl wendet alle noch ausstehenden Migrationsänderungen an und synchronisiert die Datenbankstruktur mit den definierten Modellen. Falls keine Migrationen anstehen, erscheint die Meldung "No migrations to apply".
	
#### 3.2 Server starten
3. **Starten Sie den Server**:
	```python manage.py runserver```
	
Mit diesem Befehl wird der lokale Entwicklungsserver gestartet. Die Anwendung ist nun unter der URL http://127.0.0.1:8000 erreichbar. Klicken Sie auf den hervorgehobenen Link, um die Anwendung im Webbrowser zu öffnen.