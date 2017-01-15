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
nach einer Formel (mehrere zur Auswahl) am Unsichersten ist, und erhält auch wieder vom Benutzer eine Einordnung
 des Samples in die Klassen. 

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
Wir wollten von der Graphikaufbereitung möglichst Betriebssystem unabhängig sein, sodass wir uns für 
eine Darstellung im Browser mittels HTML entschieden. Maschinelles Lernen besitzt eine hohe Komplexität, sodass 
klar war auf schon vorhandene Bibiotheken angewiesen zu sein. Da ein Teammitglied schon in Python bewandert war, 
insbesondere in diesem Bereich, viel die Wahl sofort auf Python für unsere Logikschicht.

Genaueres zur Installation des Python-Teils der Anwendung: **Installation Manual.md**

### Python application
Eine GUI-Beschreibung mit allen Funktionalitäten findet sich in: **Frontend Manual.md**

Dokumentation der Plannung des Frameworks in: **Active Learning Framework Planning Phase.md**



### Webserver
Der Webserver stellt einen Zugang zu allen gesammelten Datensätzen bereit und zusätzlich einige Filter, 
sowie noch Zählfunktionalitäten. Genaue Funktionsweisen finden sich in der API Dokumentation: **API.md**

## Data Exploration and Prediction Model
### Features
* hier kommen unsere Überlegungen zu den Features rein
#### Genutzte:
* **verwendete Sprachen**: Vektor mit den genutzen Sprachen des Repos
* **Reponame**:
* **Autorname**:
* **Description**: 
* **Readme**:
* **Filenamen**:
* **Ordnernamen**:


#### Rausgefallene:
* **Commitnachrichten** einzubeziehen hätte für den Featurevektor eine viel höhere Dimension bedeutet
dies hätte eine noch viel höhere Testsamplezahl bedeutet. Dahingegen aber wohl kaum relevante Informationen
hinzugefügt. Nach unserer Einschätzung sind die Kosten also zu hoch um dieses Feature zu nutzen.
* **commit_count**: Anzahl der Commits: Dieser ist herausgefallen, da keine Korrelation zu bestimmter Klasse
feststellbar war.
* **Count of filenames with min. Lev-Distanz**: Anzahl der Dateinamen mit der kleinsten Lev-Distanz aller Dateinamen
 zueinander (nicht implementiert), hätte vielleicht bessere Ergebnisse bringen können als die 
 durchschnittliche Lev-Distanz bringen können, insbesondere für HW oder DOCs, indenen gerne mal Dateinamen bis auf
 eine Zahl gleich sind.

#### unbekannte Kategorie:
* **hasDownload**: Wahrheitswert ob sich das Repo direkt downloaden lässt.
* **watches**: Anzahl Personen die Mitteilungen über pull requests und issues haben wollen über dieses Repo
* **folder_count**: Anzahl der Ordner des Repos: ist aber nach oben beschränkt, weil nur bestimmte Menge API-Calls
dafür aufgewendet werden.
* **treeDepth**: Tiefe des Ordnerbaums: kann auch wieder durch API-Calls kleiner sein als es eigentlich ist
* **stars**: Anzahl der Personen, die sich das Repo merken wollen.
* **branch_count**: Anzahl der derzeit genutzten Branches
* **forks**: Anzahl der Forks dieses Repos
* **commit_interval_avg**: durchschnittles Intervall indem Commits getätigt wurden
* **contributors_count**: Anzahl der Mitarbeiter am Repo
* **open_issues_count**: Anzahl der offenen Issues
* **avg_commit_length**: durchschnittliche Textlänge einer Commitnachricht
* **hasWiki**: Wahrheitswert für das Vorhandensein eines Wikis
* **file_count**: Anzahl der Dateien: ist auf die oberste Ordnerebene beschränkt (?)
* **commit_interval_max**: größte Zeitspanne zwischen zwei Commits
* **isFork**: Wahrheitswert ob dieses Repo durch Forken eines anderen hervorging
* **ReadmeLength**: Anzahl der Zeichen des Readme's
* **durchschnittliche Levenshtein Distanz Ordnernamen**: 
* **durchschnittliche Levenshtein Distanz Dateinamen**:


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

<table>
	<thead>
		<tr>
			<th>Repo-Link</th>
			<th>Result</th>
		</tr>
	</thead>
	<tbody>
	<tr>
	    <td>https://github.com/ga-chicago/wdi5-homework</td>
	    <td>False</td>
    </tr>
    <tr>
	    <td>https://github.com/Aggregates/MI_HW2</td>
	    <td>False</td>
    </tr>
    <tr>
	    <td>https://github.com/datasciencelabs/2016/</td>
	    <td>False</td>
    </tr>
    <tr>
	    <td>https://github.com/githubteacher/intro-november-2015</td>
	    <td>False</td>
    </tr>
    <tr>
	    <td>https://github.com/atom/atom</td>
	    <td>False</td>
    </tr>
    <tr>
	    <td>https://github.com/jmcglone/jmcglone.github.io</td>
	    <td>False</td>
    </tr>
    <tr>
	    <td>https://github.com/hpi-swt2-exercise/java-tdd-challenge</td>
	    <td>False</td>
    </tr>
    <tr>
	    <td>https://github.com/alphagov/performanceplatform-documentation</td>
	    <td>False</td>
    </tr>
    <tr>
	    <td>https://github.com/harvesthq/how-to-walkabout</td>
	    <td>False</td>
    </tr>
    <tr>
	    <td>https://github.com/vhf/free-programming-books</td>
	    <td>False</td>
    </tr>
    <tr>
	    <td>https://github.com/d3/d3</td>
	    <td>False</td>
    </tr>
    <tr>
	    <td>https://github.com/carlosmn/CoMa-II</td>
	    <td>False</td>
    </tr>
    <tr>
	    <td>https://github.com/git/git-scm.com</td>
	    <td>False</td>
    </tr>
    <tr>
	    <td>https://github.com/PowerDNS/pdns</td>
	    <td>False</td>
    </tr>
    <tr>
	    <td>https://github.com/cmrberry/cs6300-git-practice</td>
	    <td>False</td>
    </tr>
    <tr>
	    <td>https://github.com/Sefaria/Sefaria-Project</td>
	    <td>False</td>
    </tr>
    <tr>
	    <td>https://github.com/mongodb/docs</td>
	    <td>False</td>
    </tr>
    <tr>
	    <td>https://github.com/sindresorhus/eslint-config-xo</td>
	    <td>False</td>
    </tr>
    <tr>
	    <td>https://github.com/e-books/backbone.en.douceur</td>
	    <td>False</td>
    </tr>
    <tr>
	    <td>https://github.com/erikflowers/weather-icons</td>
	    <td>False</td>
    </tr>
    <tr>
	    <td>https://github.com/tensorflow/tensorflow</td>
	    <td>False</td>
    </tr>
    <tr>
	    <td>https://github.com/cs231n/cs231n.github.io</td>
	    <td>False</td>
    </tr>
    <tr>
	    <td>https://github.com/m2mtech/smashtag-2015</td>
	    <td>False</td>
    </tr>
    <tr>
	    <td>https://github.com/openaddresses/openaddresses</td>
	    <td>False</td>
    </tr>
    <tr>
	    <td>https://github.com/benbalter/congressional-districts</td>
	    <td>False</td>
    </tr>
    <tr>
	    <td>https://github.com/Chicago/food-inspections-evaluation</td>
	    <td>False</td>
    </tr>
    <tr>
	    <td>https://github.com/OpenInstitute/OpenDuka</td>
	    <td>False</td>
    </tr>
    <tr>
	    <td>https://github.com/OpenInstitute/OpenDuka</td>
	    <td>False</td>
    </tr>
    <tr>
	    <td>https://github.com/bhuga/bhuga.net</td>
	    <td>False</td>
    </tr>
    <tr>
	    <td>https://github.com/macloo/just_enough_code</td>
	    <td>False</td>
    </tr>
    <tr>
	    <td>https://github.com/hughperkins/howto-jenkins-ssl</td>
	    <td>False</td>
    </tr>
	</tbody>
</table>

<table>
    <thead>
        <tr>
            <td></td>
            <td>erzielte Präzision / precision</td>
            <td>erzielte Ausbeute / recall</td>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>DEV</td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td>HW</td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td>EDU</td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td>DOCS</td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td>WEB</td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td>DATA</td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td>OTHER</td>
            <td></td>
            <td></td>
        </tr>
    </tbody>
</table>

Wir finden, dass eine höhere Genauigkeit wichtiger ist als eine hohe Ausbeute, da es für jemanden, der mittels des
Klassifizierers nach Repos einer bestimmten Klasse sucht, von Vorteil ist, wenn er lieber wenige Treffer landet,
diese dafür dann aber richtig eingestuft wurden. 
Während eine hohe Ausbeute garantieren täte, dass von denen die wir als eine Klasse eingestuft haben, auch sehr 
viele als solche erkannt werden, dabei würde aber nicht berücksichtigt wie viele falscherweise als diese Klasse eingestuften
wurden. Bei einer Suche nach Repos einer bestimmten Klasse könnten also auch viele falsche dabei sein.
Wenn die Präzision aber für alle Klassen zunimmt würde dass auch die Ausbeute erhöhen.