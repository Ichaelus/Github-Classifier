# Documentation

## Inital Approach/Planning Phase 

### Our Strategy to get our train data

Uns wurde schon recht bald bewusst, dass wir möglichst viele Datensätze von Repositories brauchen.
Da zudem das Problem eines Limits an API-Calls besteht, um an diese Daten heranzukommen,
erstellten wir eine Datenbank um diese Daten erstmal einfach nur ohne Zugangsbeschränkungen zur Verfügung zu haben.
Daraufhin begannen wir die erhaltenen Daten zu sichten und einzuordnen. 
Dazu bauten wir uns eine kleine Webseite, die uns die Informationen eines Repositories angezeigt hat
und mit der wir klassifizieren konnten. So versetzten wir uns in die Lage eines Klassifizieres, um herauszufinden
welche der nutzbaren Features wirklich wertvoll sein könnten oder welche uns sogar noch fehlten.
Durch diese Phase erkannten wir wie unterschiedlich allein die interpretativen Ansichten von 4 Personen 
aufgrund der gegebenen Klassenbeschreibungen sein können. Wir erkannten dass diese ersten Kategorisierungen 
nicht weiter verwendet werden konnten wegen der hohen Diversität unserer Einschätzungen.
Daraus ergab sich ein kompletter Neustart der Gewinnung von Trainingsdaten, da die Trainingsdaten den Erfolg eines
Klassifizierers doch maßgeblich prägen. Wir entschlossen uns aber, möglichst natürliche Klassengrenzen zu ziehen
und sie nicht so zu setzen, dass eine Klassifzierung möglichst einfach wäre.
Diesesmal klassifizierten wir immer nur alle gemeinsam, um die Einheitlichkeit der Klassifizierung sicherzustellen.
Da dies auf Dauer zu zeitaufwendig wurde, wir aber eine möglichst große Menge an Trainingsdaten brauchten, 
übernahm diese Aufgabe nur noch einer. Fehler waren damit nicht ausgeschlossen, aber widersprüchliche Einteilungen
ähnlicher Repositiories sollten dadurch relativ selten werden.
Somit kommen wir nun schlussendlich auf einen Trainingspool von ca. 2000 Repositiories.

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
Durch Active Learning ordnet man aber nach unserer Empfindung hauptsächlich Repos eine Klasse zu, die zwischen 
den Klassen stehen. Ein gutes Trainingsset stellten wir fest, braucht aber auch eine große Anzahl an Repos, 
die sich fast 100-prozentig der jeweiligen Klasse zuordnen lassen, sodass wir die Parameter um ein Repo vorgelegt
zu bekommen dafür anpassten.

Für die Entscheidung welche Features genutzt werden sollten, erstellte jeder zunächst einen Featurevektor 
(siehe Discussion/Feature Vector Ideas), sodass wir eine gute Diskussionengrundlage hatten.
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

Dazu nutzen wir unteranderem:
> Konfusionsmatrix

<img src="/Documentation/Konfusionsmatrix.png" height=350>

> Kreisdiagramm

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

#### Text
Early on we agreed on a distinction of numerical features and text features such as readme and description.
While it is no problem to feed numerical features directly into our machine-learning model of choice, 
we tried multiple approaches of how to encode the text presented to us.

> **Frequency-based methods:** We count the frequency of specific tokens or words in our documents and 
therefore encode the text in a sparse vector with each element representing how often one specific word/token occurs (large number = high frequency).
Using this approach we had to consider how long this vector may be in order to be efficient as possible.
We only count the frequency of the __x__ most frequent terms (excluding stop-words). 
While short vectors (and therefore less words we can keep track of) allow more robust classification
results for our classifiers, we may loose important information that could make important distinctions (such as HW vs EDU) impossible.
Having this problem in mind we also used a trick to reduce the necessary dimensionality a lot by not encoding each word 
but the word stem ('library' and 'libraries' are bot represented by '__librari__').
The resulting number of necessary words/tokens turned out to differ from the text we encoded. 
We use smaller numbers (~2000) **UPDATE THOSE NUMBERS** for repository-descriptions and even less (~200) for folder-/filenames.
The readme turned out to need a lot more (~6000).  

> **Word embeddings:** An alternative approach is to not represent a document as a vector accounting for all used words 
but to represent each word as vector which holds information about the context of it. 
So we end up with a matrix where each row stands for such a wordrepresenation. This embedding is learned through algorithms 
like presented in [this paper](https://papers.nips.cc/paper/5021-distributed-representations-of-words-and-phrases-and-their-compositionality.pdf).
A so called __Word2Vec__ model pretrained on Google-News articles which has a vocabulary size of 3 million distinct words is being used herefore.
Each word-vector is fed into a recurrent neural network (explained later) one after another.

> **Buchstabe für Buchstabe mit LSTM:**
But instead of learning such a complex representation for each word we can just directly feed a text character-wise into such a network.
This method came in handy when trying to classify depending on features like the repository-name.
In many cases the name was too specific and complex to have ever appeared before and so no vector-representation is available with previous methods.  

 > **Edit distance:**
 When trying to classify repositories that belong to Homework, Documents or Education it's important to know how similar the names of files or folders are.
 Such repositories often contain folders like __Week 1, Week 2, Week 3, ...__. So to hand that information directly to our classifiers 
 we measured the average __Levenshtein distance__  of all files and folders.

> **Document vector:**
A possible approach similar to word embeddings is often refered to as __Doc2Vec__, presented [in this paper](https://cs.stanford.edu/~quocle/paragraph_vector.pdf).
While we weren't able to test this approach yet we're excited to see how it will compete against our current methods.


#### Summary of used text-features:
* **Repository-name**
* **Author-name**
* **Description**
* **Readme**
* **Filenames**
* **Foldernames**
* **Average Levenshtein distance of filenames**
* **Average Levenshtein distance of foldernames**

#### Dismissed features:
* **Commit messages** were considered to not obtain enough valuable information to sacrifice both the increase in input-dimension for the classifiers 
and necessary api-calls.
* **Commit count**: Weren't used as we didn't measure any correlation with specific classes.
* **Count of filenames with min. Lev-Distanz**: Could be more informative for classes like __HW__ or __DOCS__ than the average Levenshtein distance and might be implemented in the future. 

#### Metadata:
* **hasDownload**: Boolean value if repository can be downloaded directly.
* **watches**: Count of people who follow latest news in respect to new pull requests and issues that are created.
* **folder_count**: Count of folders is currently limited due to limited api-calls available.
* **treeDepth**: Depth of folder-structure. Also capped at the moment due to limited api-calls.
* **stars**: Count of people who use this notification system.
* **branch_count**: Count of branches currently in use.
* **forks**: Count of created forks.
* **commit_interval_avg**: Average interval in which commits where created.
* **contributors_count**: Count of contributors to this repository.
* **open_issues_count**: Count of open issue.
* **avg_commit_length**: Average text-length of commit messages.
* **hasWiki**: Boolean value if wiki is available.
* **file_count**: Count of files in first layer of folder-structure (Where readme is usually located).
* **commit_interval_max**: Longest interval between commits.
* **isFork**: Boolean value if repository is fork of another.
* **ReadmeLength**: Count of characters in readme.
* **verwendete Sprachen**: Used programming languages (represented as vector with each column representing one language. 0.5 if language is beeing used, 1.0 if it's the repository's main language).



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
Eine Betrachtung des Fscore, wodurch es möglich ist sowohl Präzision als auch Ausbeute in einen Wert zu fassen, mit höherer Gewichtung der Präzision empfinden wir aber als die bessere Wahl, da dadurch die Ausbeute nicht völlig aus der Betrachtung fällt.
