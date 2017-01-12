# Documentation

"Please also document the decisions you made selecting your features, 
algorithms, data structures and software development tools and practices."

## Inital Approach/Planning Phase 

### Our Strategy to get our train data
* Api-Call Limit, erste Website
Uns wurde schon recht bald bewusst, dass wir möglichst viele Datensätze von Repositories brauchen.
Da zudem das Problem eines Limits an API-Calls besteht, um an diese Daten heranzukommen,
erstellten wir eine Datenbank um diese Daten erstmal einfach nur ohne Zugangsbeschränkungen zur Verfügung zu haben.
Daraufhin begannen wir die erhaltenen Daten zu sichten und einzuordnen. 
Besonders geholfen hat uns dabei eine kleine Webseite, die uns die Informationen eines Repositories angezeigt hat
und mit der wir klassifizieren konnten. So versetzten wir uns in die Lage eines Klassifizieres, um herauszufinden
welche der nutzbaren Features wirklich wertvoll sein könnten oder welche uns sogar noch fehlten.
Durch diese Phase erkannten wir wie unterschiedlich allein die interpretativen Ansichten von 4 Personen 
aufgrund der gegebenen Klassenbeschreibungen sein können. Wir erkannten dass diese ersten Kategorisierungen 
nicht weiter verwendet werden konnten wegen der hohen Diversität.

### First Data Set Impressions
* Erste Versuche mit ersten Classifiern/Entdecken des Majority Class Problems
* Erste Überlegungen zu den Features
Erste Versuche starteten wir mit neuronalen Netzwerken und Support Vector Maschines (zu finden unter **First Trys**).
Theoretische Überlegungen waren uns zu diesem Zeitpunkt aber wichtiger. Eine war:
"Inwiefern beeinflusst das Majority Class Problem unseren Klassifizierer"
Wir fanden nämlich heraus, dass die Klasse **development** um ein vielfaches häufiger vorkommt als alle anderen Klassen.
Daraus entstand die Idee erst nur zwischen **DEV** und **nicht DEV** entscheiden zu lassen und danach 
dann **nicht DEV** in die weiteren Klassen aufzusplitten (s. classification-skizze.png), sodass wir nicht mit einem 
Majority Class Problem konfrontiert waren.
Dies verfolgten wir aber nicht weiter, weil wir der Meinung waren, dass sich das Problem über class raids 
lösen lässt, indem die Gewichtung von **DEV** und **Nicht DEV** Samples unterschiedlich gestaltet wird.
Weiterhin entschieden wir uns später noch Active Learning einzusetzen. Dies ermöglichte uns aus unserem Pool 
an ungelabelten Daten (etwa 30000 Repositories), die Samples herauszusuchen, die besonders interessant für das 
Trainieren wären. Dafür entschieden wir uns auf 2 Modi zu setzen. Einmal wird aus dem Pool ein zufälliges
Repository entnommen, falls die Klassifizierer sich unsicher mit der Einschätzung dieses sind, wird der
Benutzer befragt.
Im anderen Modus darf sich reihum ein Klassifizierer ein Sample aus dem Pool herauspicken, bei dem er sich
nach einer Formel am Unsichersten ist, und erhält auch wieder vom Benutzer eine Einordnung des Samples
in die Klassen. 

Jeder erstelle zunächst einen Featurevektor (siehe Discussion/Feature Vector Ideas), sodass wir eine gute 
Diskussionengrundlage hatten.
Als erste konventionelle Features kristallisierten sich die textuellen Daten heraus, darunter: Readme,
Kurzbeschreibung, Ordnernamen, Dateinamen, Autorname. Bei Ordner und Dateien mussten wir wegen des API-Call Limits
uns auf die oberste Ebene beschränken. In Diskussionen einigten wir uns auch der Verlockung durch festgelegte
Schlüsselwörter zu widerstehen, Mustererkennung sollte dem Klassifizierer überlassen bleiben.
Neben den sprachabhängigen Features fanden wir auch Features der Projektstruktur: Hauptprogrammiersprache, 
vorkommende Programmiersprachen, Ordnertiefe, Anzahl Commits, durchschnittliche Commitlänge, Anzahl Branches, 
hat Downloads, Ordneranzahl, Dateianzahl und weitere. Später kam noch die durchschnittliche Levenshtein Distanz
sowohl zwischen Ordner als auch Files dazu, weil uns auffiel, dass wir bis jetzt noch nicht berücksichtigt hatten, 
dass bei DOCS oder HW Ordner/Filenamen meist oftmals ähnlich sind.


### Discussions about Class Descriptions
Die Klassenbeschreibungen fanden wir nicht so eindeutig, sodass wir uns entschieden haben,
die gegebenen Klassenbeschreibungen an den wunden Punkten in unseren Augen zu korrigieren.
Dadurch haben wir dann herausgefunden zwischen welchen Klassen einordnungsprobleme bestehen,
also wie sich jeweils 2 der gegebenen Klassen zueinander abgrenzen.
Diskussionsergebnisse sind in **Classification Ambiguities.md** zu finden.

## Software Architecture

### Goals
* MainlyReusability, make it as easy as possible to try and compare different solutions etc
Possibily also for other projects

Die Anwendung soll uns Active Learning Unterstützung zur Verfügung stellen, sowie eine Testumgebung
für die Klassifizierer bereitstellen.
Weiter soll sie möglichst gut mit verschiedensten Klassifizierern arbeiten können, sodass 
ein schnelles Testen dieser möglich wäre (Austauschbarkeit der Klassifizierer).
Darüberhinaus soll die Anwendung uns Informationen über die Güte der erfolgten Klassifizierungen
liefern können.

Konfusionsmatrix
<img src="/Documentation/Konfusionsmatrix.png" height=350>
Kreisdiagramm
<img src="/Documentation/Kreisdiagramm.png" height=350>

### Overview
Grundsätzlich ist unsere Anwendung in einen php-Server mit Datenbank und einen lokalen Phython-Bottle-Server
aufgeteilt. Der php-Server übernimmt dabei den Teil des Repositories zu Datensätzen Aufbereitens und die 
Speicherung aller bisher gewonnen Datensätze. 
Wir wollten von der graphikaufbereitung möglichst Betriebssystem unabhängig sein, sodass wir uns für 
eine Darstellung im Browser mittels HTML entschieden. Maschinelles Lernen besitzt eine hohe Komplexität, sodass 
klar war auf schon vorhandene Bibiotheken angewiesen zu sein. Da ein Teammitglied schon in Python bewandert war, 
insbesondere in diesem Bereich, viel die Wahl sofort auf Python für unsere Logikschicht.

### Python application
### Webserver

## Data Exploration and Prediction Model
### Features
* hier kommen unsere Überlegungen zu den Features rein


#### Rausgefallene:

* Commitnachrichten einzubeziehen hätte für den Featurevektor eine viel höhere Dimension bedeutet
dies hätte eine noch viel höhere Testsamplezahl bedeutet. Dahingegen aber wohl kaum relevante Informationen
hinzugefügt. Nach unserer Einschätzung sind die Kosten also zu hoch um dieses Feature zu nutzen.

### Prediction Model
* hier kommen unsere Überlegungen zu den Classifiern rein

### Example Repositories
"Please document three repositories where you assume that your 
application will yield better results as compared to the results of other teams."
Hinweise um solche bei uns zu finden:
* HW/DOC könnte durch Levenshtein Distanz besser sein...
* ??

## Validation
"Apply your classifier on the repositories included in  Appendix B . 
You can find this file on https://github.com/InformatiCup/InformatiCup2017 as well. 
Create a boolean matrix where you compare the results where you compare the results of your 
classifier and your intuitive classification (if your intuitive classification matches the output 
of your program, the element in the matrix will result to true, otherwise to false).
Compute the recall per category- the number of repositories intuitively placed within a 
category in the set of repositories that got placed in the same category by your classifier.
Compute the  precision per category- the number of repositories per category where the results 
determined by your automatic classifier matched your intuitive classification.
Discuss the quality of your results and argue whether, according to your opinion, 
a higher yield or a higher precision is more important for automated repository classification."
