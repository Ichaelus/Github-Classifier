# Active Learning Framework Planning Phase

## Libaries we´re using
* threading for Threads
* pickle for serialization
* bottle for communication with GUI

# Saving System 
* We have one Folder for saving stuff
* in this folder there´s going to be one file for the classifier collection:
    what classifiers are currently loaded etc.
* Each classifier modul has it´s own subfolder there. We have one file with the information what´s the 
    version that got used last and all other information we may need to safe seperate, then all the safefiles
    of the different versions of the same classifier

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
    Stefan: Kann man ja trotzdem machen, aber vlt will man diese ja dann irgendwann zusammengesteckt trainieren und trotzdem
            nur jedes 10. sample oder so zum trainieren der Gewichtigungen verwenden, war jetzt mein Gedanke

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
* start-live-training(bool: unsupervisedlearningmode) (): aka play button
    unsupervisedlearningmode: wenn sich alle Klassifikatoren sicher sind, dann könnten wir vor dem nächstem Schritt das jeweilige Sample
    noch zum trainieren verwenden
* do live-training-step():
    classifiy/train/calculate uncertainty for the next (1) repo 
* Funktion um nur einzelne Klassifizierungsmodule mit bestimmten Samples zu trainieren
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
* Stefan: Hatte das jetzt nicht als Ensemble-learning geplant, sondern nur als Sammlung mehrerer Klassifikations-Module damit man die 
        nicht immer alle einzeln laden und speichern muss, weiß aber nicht wie sinnvoll das ist. Können auch durchaus nochmal 
        fürs Ensemble-Learning eine eigene Klasse verwenden (oder ist die classificator collection überflüssig und wir wollen sie hierfür verwenden?)
        Wichtig hierbei wäre, das man relativ bequem die vorherigen Klassifikatoren als Bausteine verwenden kann die bereits vorher vortrainiert wurden,
        aber vlt will man trotzdem beim Ensemble-Learning die einzelnen verwenden Klassifikatoren nachtrainieren.
* consists of several Classificator Moduls to train them at the same time with active learning 
* Is responsible to coordinate each round and to forward function calls to each classificator
    and to check if a classificator is unsure about something
* Es wäre sinnvoll wenn wir in jeder Session immer sehen welches Klassifizierungsmodul für wieviele 
    Nachfragen beim Benutzer verantwortlich ist
* Fürs Semi-Supervised Learning wäre es vlt sinnvoll dass man auch festlegen kann dass nur dann Samples zum Trainieren verwendet werden wenn eine 
    bestimmte Anzahl, zum Bsp alle Klassifikatoren sich sicher sind mit der Kategorie (evtl könnte man das muten auch hier reinspielen lassen)
* Wollen wir Kontrollen einfügen, wo wir ab und zu Samples die bereits klassifiziert wurden zum Supervised Learning verwendet werden
    und wir einen Alarm bekommen wenn er jetzt damit Schmarrn gemacht hätte (also falsche Klasse und zum Trainieren verwenden)?



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
* detailled-prediction(sample):
    So etwas würden wir brauchen wenn wir später einzelne Klassifikatoren als Bausteine in Ensemble-Learning verwenden wollen, aber 
    wahrscheinlich ist es unmöglich hier einen gemeinsamen Standard festzulegen oder? Intuitiv würde sich hier die Wahrscheinlichkeit
    dass etwas in einer gegeben Klasse ist anbieten, aber wahrscheinlich bekommt man die nicht von jedem Lern-Algorithmus
    Außerdem ist hier zu beachten (und auch bei der predict-classe Methode 1 weiter oben), dass nicht alle die Klasse vorhersagen sollen,
    sondern manche nur z.b. DEV oder NICHT DEV. Mit Wahrscheinlichkeiten würde sich das hier so lösen lassen dass man sagt
    man hat nur die DEV-Wahrscheinlichkeit zwischen 0 und 100% und die anderen Wahrscheinlichkeiten sind immer 0% oder sowas
    Aber wahrscheinlich sind nicht alle fälle so schön zu lösen und wir müssen uns hier nochmal was überlegen
    (Z.B. wenn wir einen Klassifikator haben der sagt ob etwas in "HW oder EDU" oder nicht ist)
* get-name():
    Gibt den Namen des Klassifikators zurück
* get-description():
    Gibt eine kurze Beschreibung zu dem Klassifikator zurück
* format-input-data():
    Wird nur intern verwendet, hier wäre es eventuell sinnvoll ein kleines Libary File mit unterschiedlichen Formatierungen aufzubaun
    (alles in einem Vektor, nur die Readme, nur die Metadaten usw.)
* mute-classificator(classificator):
    Der Klassifikator verursacht keine Nachfragen beim Nutzer mehr

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
    * get-description():
        Immer gut wenn man sich nicht mehr daran erinnert was man sich zu einem einzelnem Klassifizierer gedacht hat

* Stefan: Ja ist wahrscheinlich die beste Möglichkeit das immer auf diese Art und Weise abzuspeichern

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

## API-Funktionen die wir eventuell noch brauchen
* Funktion die eine bestimmte Anzahl an zufällig ausgewählten Repos zurückgibt




