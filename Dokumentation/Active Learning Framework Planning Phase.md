# Active Learning Framework Planning Phase

## Important Points

* Evtl. ist es sinnvoll bei jeder Speicherung einen TimeStamp mitzuspeichern
* Wie viel wollen wir Ensemble-Learning verwenden, lohnt es sich hier ausführlich die Struktur zu modularisieren?
    * Andi: Ein Blick auf "https://en.wikipedia.org/wiki/Ensemble_learning" lässt vermuten, dass das Testen verschiedener Methoden sinnvoll ist.
            Hierfür wäre es hilfreich, solch eine Schnittstelle/ Klasse zu vereinbaren.
* Bereits relativ früh eine graphische Oberfläche zu haben könnte sehr wertvoll sein!
* In der DB eine zusätzliche Tabelle für durch Klassifizierer sicher klassifizierte Repos zum Semi-Supervised-Learning?

## Issues we need to deal with

* Manche Klassifizierungsmodule, vor allem solche, die Ensemble-Learning verwenden, müssen wissen, wieviele Trainingsdaten
    verfügbar sind, z.B. wenn verschiedene Klassifikatoren für unterschiedliche Features verwendet werden, z.b. 90% 
    der Daten werden zum Trainieren der Klassifikatoren verwendet und die letzten 10% für das Trainieren der Gewichtungen
    der unterschiedlichen Klassifikatoren
    Andi: Sicher? Wieso nicht seperates Trainieren und Lernen von Gewichtungen einzelner Classifier mit gleichen Trainingsdaten?

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

* Andi: So wie ich das verstehe, wird hier das Ensemble-Learning vollzogen.
        Deshalb würde ich vorschlagen, fast ausschließlich alle Funktionen im vorherigen Absatz hier als Methoden aufzunehmen.
* consists of several Classificator Moduls to train them at the same time with active learning 
* Is responsible to coordinate each round and to forward function calls to each classificator
    and to check if a classificator is unsure about something
* Es wäre sinnvoll wenn wir in jeder Session immer sehen welches Klassifizierungsmodul für wieviele 
    Nachfragen beim Benutzer verantwortlich ist



## Functions a Classification Module needs to provide

* safe/load-status():
    Die Methode, welche von den safe/load-Methoden oben dann jeweils für jeden Klassifikator verwendet werden
* reset-all-training():
    Klassifikator wird auf den Status vor dem ganzen Training zurückgesetzt
* get-uncertainty():
    gibt Unsicherheit zurück (wollen wir das als boolean oder als float zwischen 0 und 1 machen?)
    Andi: Je nachdem, ob Threshold für sicher/unsicher von jew. Modul abhängt oder global für alle definiert ist.
* train-on-sample(sample, class, nb_old_data):
    Trainiere (inkrementell) mit Sample. Evtl zusätzlich mit best. Menge alter Daten, damit overfitten auf neue Daten verhindert wird.
* train(samples, classes):
    Trainiere mit Liste von Daten. Evtl weitere Paramter nötig (nb_epoch, learning_rate, ...)
* predict-class(sample):
    Gibt zurück, wie der Klassifikator ein gegebenes Sample klassifizieren würde
* get-name():
    Gibt den Namen des Klassifikators zurück
* get-description():
    Gibt eine kurze Beschreibung zu dem Klassifikator zurück
* format-input-data():
    Wird nur intern verwendet, hier wäre es eventuell sinnvoll ein kleines Libary File mit unterschiedlichen Formatierungen aufzubaun
    (alles in einem Vektor, nur die Readme, nur die Metadaten usw.)

## Classifier State Module sinnvoll?
* Attribute:
    * Zeit
    * Notizen
    * versch. Metriken für Qualität des Classifiers zu diesem Zeitpunkt
    * Parameter/ State des Classifiers für evtl Backup
* Methoden:
    * get-accuracy (Je nach Metrik)
    * get-Classifier
    * get-notes
    * get-timestamp

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
* process-readme(readme_text)
* process-description(description_test)

* verschiedene Datenformatierungsmethoden
* verschiedene Methoden um Daten aus unserer DB zu holen





