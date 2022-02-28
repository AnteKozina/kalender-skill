# Dokumentation MyCroft Projekt 

Gruppenmitglieder: 
- Bastian Wiggenhauser (bw040) 
- Ante Kozina (ak265)

# Aufgabenstellung
In diesem Projekt haben wir die Aufgabe, einen eigenen MyCroft-Skill zu erstellen, der es erlaubt, Informationen aus einem hinterlegten Kalender abzufragen. Die Interaktion soll über den mycroft-cli-client sowie auch per Spracheingabe möglich sein (die Eingabe über den mycroft-cli-client ist hierbei robuster).

Zwei Interaktionen sind Pflicht bei dem Projekt:
1. Abfrage nach dem nächsten Termin
1. Abfrage nach den Termin eines bestimmten Tages

Weitere Interaktionen sind Bonusaufgaben:
1. Erstellen eines neuen Termins
1. Löschen eines bestehenden Termins
1. Umbenennen eines bestehenden Termins

Die Implementierung soll in Python geschehen. Dabei sollen wir darauf achten, die [Google Coding Styles](https://google.github.io/styleguide/pyguide.html) zu min. 50% einzuhalten.

Final sollen wir zu diesem Projekt noch eine Dokumentation verfassen.

# Erläuterung unserer Vorgehensweise
Zunächst haben wir uns die [Dokumentation von MyCroft](https://mycroft-ai.gitbook.io/docs/skill-development/introduction/your-first-skill) auf der entsprechenden Internetseite gelesen, um den Skill richtig anlegen zu können. Analog zu dieser Anleitung haben wir MyCroft dann eingerichtet, zusätzlich haben wir uns auf der Nextcloud-HdM-Seite registriert, um Zugriff zum Kalender zu bekommen, der angebunden werden soll.

Dann mussten wir uns entscheiden, ob wir ein GitHub oder ein GitLab Repository verwenden, die Wahl fiel schlussendlich dann auf GitHub. Dort haben wir das Repository erstellt.

Sobald der Skill auf unserem Raspberry Pi installiert und mit unserem Repository verbunden war, haben wir getestet, ob der Skill soweit funktioniert. Hierbei haben wir auch ausprobiert, ob die Spracheingabe funktioniert, und nach einigem Ausprobieren haben die beiden Anwendungsfälle dann auch geklappt.

Nachdem das funktioniert hat, haben wir uns einige Internetressourcen zu CalDav in Verbindung mit Python angeschaut, damit wir die Kalender-Interaktion umsetzen können. Dazu gab es erfreulicherweise viele Anleitungen.

Nachdem wir wussten, wie wir den Kalender ansprechen können, haben wir zunächst die grundlegenden Kalenderfunktionen implementiert:
- Abruf aller Events
- Abruf des nächsten Events
- Abruf aller Events eines bestimmten Tages

Diese Implementierung ist zunächst in der caldav_starter.py-Datei geschehen. Wenn alles funktiniert hat, haben wir den Code in die \_\_init__.py übernommen.

Bei der Implementierung sind wir auf einen Fehler gestoßen: Das Verteilen von unterschiedlicher Funktionalität auf mehrere Python-Dateien hat in Verbindung mit MyCroft nicht funktioniert. Dies war merkwürdig, da es in Tests auf einem Windows-Rechner problemlos funktioniert hat. Gelöst haben wir das Problem, indem der vollständige Python-Code sich in einer einzigen Datei befindet: 

    __init__.py

Dieses Problem hat uns dazu gebracht, auf verschiedenen Branches zu arbeiten, um auf dem Master immer ein lauffähiges Projekt zu haben. Die Entwicklungsarbeit ist auf dem dev-Branch passiert, nach erfolgreicher Implementierung wurden die Ergebnisse dann in den Master-Branch gemerged.

Als die Anbindung an den Kalender soweit funktioniert hat, haben wir dem Skill implementiert: Dabei haben wir zunächst die jeweiligen .intent-Dateien angelegt, die für jeden Skill nötig sind. In diesem Dateien steht in Textform, worauf MyCroft später reagieren soll. In diesen Dateien haben wir zusätzlich Entities definiert, die aus der Spracheingabe ausgelesen und im Code direkt verwendet werden können.
Folgende Entities haben wir verwendet:
    
    - day.entity
    - month.entity
    - year.entity

Damit diese Entities zur Kalenderinteraktion verwendet werden können, haben wir drei Helper-Funktionen geschrieben, die zurückgeben, ob es sich jeweils um einen validen Tages-, Monats- oder Jahreswert handelt. Diese Helper-Funktionen sind aus vorher genannten Gründen ebenfalls in der \_\_init__.py zu finden. Aus Software-Architektursicht sind das aber Funktionen, die eigentlich in separate Klassen gehören.

Anschließend haben wir versucht, die Anmeldedaten für den Kalender über ein settingsmeta.yaml einzubinden. Der Plan war es, dass beim Herunterladen des Skills die Anmeldedaten auf der Website eingegeben werden und dadurch in der settingsmeta.yaml-Datei landen. Das hat aber nicht funktioniert, daher sind die Anmeldedaten in der settings.json zu finden. Würde dieses Projekt weitergeführt werden, wäre ein vollständiges Entfernen der Anmeldedaten aus dem Code der logische, nächste Schritt.

## Bonusaufgaben
Dann haben wir die Bonusaufgaben umgesetzt, zuerst die Event-Erstellung, dann das Löschen und schließlich das Umbenennen.


# Erläuterung unseres Konzepts
Alles geschieht in der \_\_init__.py. Ein neuer Kalender wird angelegt, die Anmeldedaten kommen aus der settings.json. In der Kalenderklasse sind verschiedene Intent-Handler zu finden, die jeweils eine Interaktion mit dem Nutzer behandeln.

Jeder Intent-Handler hat Zugriff auf die Entities, die in der Nachricht zu finden sind.

Mithilfe dieser Entities rufen die Intent-Handler die unten gegebenen Kalender-Funktionen auf. Diese Kalenderfunktionen rufen die relevanten Funktionen vom Kalender ab, bauen die Informationen in einen String ein und geben diesen an den Intent-Handler zurück.
Dieser String wird dann durch den Intent-Handler an den Benutzer ausgegeben.

Beim Löschen und Umbenennen eines Events wird das Datum des Events abgesucht. Mit dem dabei gefundenen Event wird dann weiter gearbeitet (wird gelöscht oder umbenannt).


# Neuen Mycroft Skill anlegen
Mit dem Befehl

    mycroft-msk create

kann man einen Skill generieren.
Nach dem Befehl und dem Durchlaufen einiger Fragen wird der Skill im Verzeichnis 
        
        /opt/mycroft/skills 
        
abgelegt.

Weitere Hinweise und Anleitungen können hier gefunden werden:
- [MyCroft Dokumentation: Your first skill](https://mycroft-ai.gitbook.io/docs/skill-development/introduction/your-first-skill)
- [MyCroft Dokumentation: Skill structure](https://mycroft-ai.gitbook.io/docs/skill-development/skill-structure)

# Hinweise
Hier sind noch einige wichtige Hinweise zu finden:
- Wenn die Abfrage nach den Events eines bestimmten Tages per mycroft-cli-client-Eingabe gestellt wird, muss der Tag (die Zahl) aus zwei Ziffern bestehen, also z.B. 01 statt 1. Bei der Eingabe einer einzelnen Ziffer wird ein anderer Skill gestartet.

# Fazit und Ausblick

### Was wir gelernt haben:
Zunächst gelernt haben wir den Umgang mit ical-Objekten, die ein Standard im Web bei der Verwendung von Kalendern sind. Des Weiteren haben sich unsere Python-Skills verbessert, und durch die Verwendung eines Python Linters und durch die Google Coding Styles haben wir auch gelernt, besseren Python-Code zu schreiben. Außerdem haben wir eine Open Source Alternative zu den bekannten Sprachassistenten von Google, Apple und Amazon kennen gelernt.

### Wie man den Skill weiterentwickeln könnte
Ein Kalender, bei dem man nur so wenige Funktionen hat wie unser Kalender, ist noch nicht besonders nützlich. Mehr Funktionen wären hier sinnvoll, z.B. das Anlegen von zusätzlichen Informationen pro Termin, das Anlegen von wiederkehrenden Terminen, Einladungen für bestimmte Termine zu verschicken, und so weiter, die Möglichkeiten sind nahezu endlos.

Technisch wäre es auch nötig, die Anmeldedaten komplett aus dem Code zu nehmen und dies über die MyCroft-Seite zu regeln. Hinsichtlich der Sicherheit besteht momentan ein Problem bei uns, da die Anmeldedaten mit im Repository zu finden sind. Da das Repository aber privat ist, die Anmeldedaten nach Ablauf des Semesters ohnehin nicht mehr funktionieren und das Testen unseres Programms dadurch deutlich erleichert wurde, haben wir uns entschieden, dies so zu lassen. In einer echten Produktion wäre das ein großer Fehler, dessen sind wir uns selbstverständlich bewusst.

Auch wäre es sicherlich hilfreich herauszufinden, warum die Aufteilung auf mehrere Klassen nicht funktioniert hat, da die Datei \_\_init__.py sehr schnell groß und unübersichtlich wird.

# Anhang
### Funktionierende mycroft-cli-client Befehle (als Beispiel)
whats my next appointment

[HIER NOCH HINZUFÜGEN]