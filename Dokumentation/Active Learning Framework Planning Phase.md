# Active Learning Framework Planning Phase

## Important Points

* Evtl. ist es sinnvoll bei jeder Speicherung einen TimeStamp mitzuspeichern
* Wie viel wollen wir Ensemble-Learning verwenden, lohnt es sich hier ausführlich die Struktur zu modularisieren?
* Bereits relativ früh eine graphische Oberfläche zu haben könnte sehr wertvoll sein!

## Functions User Can Call Manually

* collect-important-examples(data):
    Testet Beispiele aus dem Pool von ungelabelten Daten auf Wichtigkeit und fügt wichtige Repos zu eigener DB Tabelle hinzu.
    Diese Einträge können wir dann später auf der Website klassifizieren und werden anschließend zum Pool an gelabelten Daten hinzugefügt
* load/save-classificator-collection():
    Standardmäßig sollte das zuletzt genutzte Setup wieder geladen werden, optional aber evtl auch andere vorher hinzugefügte.
    Speichern: Immer mit TimeStamps; dies soll hauptsätzlich dazu dienen eine Ansammlung von Classificatoren gleichzeitig inkrementell
    trainieren zu können
* remove/add-classificator():
    Dies ist auch vor allem nützlich weil man eventuell unterschiedliche Versionen desselben Classificators hat die zu unterschiedlichen
    Zeitpunkten unterschiedlich trainiert wurden
* start-live-training(bool: unsupervisedlearningmode):
    unsupervisedlearningmode: wenn sich alle Klassifikatoren sicher sind, dann könnten wir vor dem nächstem Schritt das jeweilige Sample
    noch zum trainieren verwenden
* pause-live-training():
    bringt noch die akutelle Runde zu Ende? und wartet dann auf weitere Befehle
* resume-live-learning():
* calucate/save-fitness-of-all-classificators():
    Mit Gui könte man immer 2 Fitness-Werte-Sammlungen anzeigen: Einmal die zuletzt gespeicherte und einmal die aktuelle Klassifizierungsrate
    der verschiedenen Klassifikatoren, diese könnten wir in festen Zeit-Intervallen immer wieder berechnen und die Verbesserung/Verschlechterung
    in Prozent anzeigen, ist vlt ganz interessant zum Live-Training im supervised mode
* detailled-fitness(): 
    Gibt auf Wunsch ganz ausführliche Auskunft über die aktuelle Fitness: welcher Klassifikator ist wie gut im Umgang mit welcher Klasse usw 
    (graphische Aufbereitung!)
* undo-last-training():
    Wir könnten immer vorm Trainieren automatisch speichern und damit wieder zu dem Speicherpunkt zurrückkehren, z.B. wenn wir feststellen,
    dass das letzte Training eine signifikate Fitness-Einbuße gebracht hat
* safe-classificator-status(classificator)
* train-all-classificators(data):
    klassiches Trainieren aller Klassifikatoren

## Classificator collection

* consists of several Classificator Moduls to train them at the same time with active learning 
* Is responsible to coordinate each round and to forward function calls to each classificator
    and to check if a classificator is unsure about something



## Functions a Classification Module needs to provide

* safe/load-status():
    Die Methode, welche von den safe/load-Methoden oben dann jeweils für jeden Klassifikator verwendet werden
* reset-all-training():
    Klassifikator wird auf den Status vor dem ganzen Training zurückgesetzt
* get-uncertainty():
    gibt Unsicherheit zurück (wollen wir das als boolean oder als float zwischen 0 und 1 machen?)
* predict-class(sample):
    Gibt zurück, wie der Klassifikator ein gegebenes Sample klassifizieren würde
* get-name():
    Gibt den Namen des Klassifikators zurück
* get-description():
    Gibt eine kurze Beschreibung zu dem Klassifikator zurück
* format-input-data():
    Wird nur intern verwendet, hier wäre es eventuell sinnvoll ein kleines Libary File mit unterschiedlichen Formatierungen aufzubaun
    (alles in einem Vektor, nur die Readme, nur die Metadaten usw.)

## Utility Libary

* get-raw-data-from-web(repositorylink):
    fragt am Webserver die ganzen Daten an
* get-raw-data-by-myself(repositorylink):
    brauchen wir erstmal nicht, irgendwas brauchen wir aber hier vor der Abgabe
* post-user-classification():
    Um die manuellen Klassifizierungen die vom aktiv Learning angefordert wurden in den Labelled-Daten-Pool zu bekommen
* post-automatic-classificytion():
    Könnte nützlich sein, wenn sich ein oder mehrere Systeme bei einer Klassifizierung sicher sind diese auch zu speichern in einer eigenen Tabelle
    für unsupervised learning
* verschiedene Datenformatierungsmethoden
* verschiedene Methoden um Daten aus unserer DB zu holen





