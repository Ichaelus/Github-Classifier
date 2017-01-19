# Documentation

## Inital Approach/Planning Phase 

### Our Strategy to get our train data

As we approached this problem from a machine learning perspective we knew from the start that our models require a 
large and diverse collection of manually classified examples.
GitHub only grants a limited number of Api-calls available in a short amount of time so early on we stored
all hand-classified repositories with extracted features in a database to access them without restrictions.
The process of classification was made possible through a website whose aim was to display all necessary information about a repository
and made the assignment into categories possible.
In this process we filtered out all information (features) we needed and also possibly lacked to do so confidently.
Pretty soon we were suprised by how different our perspectives were in regards to which class to asign to many repositores.
Following this we decided to abolish all samples we classified through weeks and start from the beginning.
The danger this diversity proposed to our classification-results was unacceptable.
So we worked out precise definitions of each class and listed vital edge cases.
The focus hereby laid on understandable definitions, finally sacrificing better evaluation scores of our models since 
many important distinctions are very hard 'to get' for these models. **MAYBE EMPHASIS THIS MORE?**
After we learned from our mistakes we started to only classify in groups, later on handing this task over to only two team members
and finally to only one person as it became too time-consuming.
Mistakes made by this one person couldn't be prevented but eliminating the possibility of confusing differences in proposed classifications
was our priority.
Using this method we finally classified over 2000 repositories by hand in the course of one month. **FIND BETTER TIME-WINDOW**


### First Data Set Impressions
* Erste Versuche mit ersten Classifiern/Entdecken des Majority Class Problems
* Erste Überlegungen zu den Features


Erste Versuche starteten wir mit neuronalen Netzwerken und Support Vector Maschines (zu finden unter **First Trys**).
Theoretische Überlegungen waren uns zu diesem Zeitpunkt aber wichtiger. **Das vlt rauslassen und erst bei classifiers erwähnen?**

After building up our first set of training-data we were confronted with a serious problem:
We encounterd a so called Majority Class Problem. As GitHub is mainly used for software development projects the class
**Development (DEV)** appeared way more frequently as any other class, taking up around 80% of all public repositories on GitHub. **Better %?**
This resulted in our first classifiers assigning *DEV* to almost every repository. **Explanation?**
Our first approach to this problem was to split up the prediction process into a first step where only the distinction between *DEV* and *NOT Dev* 
has to been made. If it was classified as *NOT Dev* we'd show the repository to a classifier which only knew how to classify such 
(see classification-skizze.png for more).
We dropped this technique later on as we started to weight the importance of each sample during training with respect to the frequency of it's class.

Furthermore we incorporated the use of *Active Learning* in our training process 
([click here for more information](https://goo.gl/TPWjGo)).
By this we were able to only present such repositories to us for manual classification which our classifiers were particularly unsure about.
We used this approach to improve our classifiers more effectively by not hand-classifying redundant repositories.
This was achieved by maintaining a large pool (~30,000) of unlabeled repositories in our database.
Two modes were implemented:
* *Stream based* One random repository from the pool is selected and shown to the classifiers. If a classifier is unsure about the class, 
the user (like an Orakel) is being questioned.
* *Pool based* In turns each classifier is shown a subset of these repositories and picks the one it's most uncertain about for further questioning.  
To measure the uncertainty about a sample, various formulas are provided.
Our experience with this method was very positive altough it turned out to not solve the issue of training altogether.
The repositories presented to the user were almost exclusively edge-cases.
On the one hand that was beneficial but in order for most of our classifiers to work correctly we needed a 
large amount of samples with clear and easy to interpret features to confirm assumptions about correlation between features.
We partly tackled this problem by adjusting the parameters which determine when a classification is assumed to be confident/unsure.


To create the optimal feature vector every team member compiled a list of possible features (see Discussion/Feature Vector Ideas).
We then discussed every proposal and added further ones.
It's notable that the features considered most important by us at first where almost exclusively text based.
Readme, description, foldernames, filenames, authorname and more. Unfortunatley we had to limit the access of our models to 
the folder and filenames of only the first layer in a repository's folder-structure. This was due to the previously mention API-Call limit.
"In Diskussionen einigten wir uns auch der Verlockung durch festgelegte
Schlüsselwörter zu widerstehen, Mustererkennung sollte dem Klassifizierer überlassen bleiben." # Soll das hier rein?
In these discussion we discovered many features we first neglected: used programming languages (with a possible emphasis on the main language),
depth of the folder-structure, commit count, average commit-length, branch count, whether a download of the repository is allowed, folder-count,
number of files and more. Later we additionally implemented the average Levenshtein distance between folder and filenames. This was done
due to a lack of any feature that can give us valuable information despite the fact that many DOCS or HW folder-/filenames are often similar.


### Discussions about Class Descriptions
As we didn't consider the class descriptions to be precise we added further explanations and
also partially changed the preexisting ones.
To examine our class descriptions and explanation of edge cases see **Classification Ambiguities.md**


## Software Architecture

### Goals
* The probably highest priority was to make it as easy as possible to try and compare different solutions. 
We tried a great variety of machine learning models (as seen later in this document) and so we needed fast interchangeability and
evaluation of models.
Additionally we wanted to make the manual classification of new repositories and training of our models so efficient 
that we can build up a great training-corpus quickly.
One step to achieve this was to integrate Active Learning in the process of selecting new training-samples.

For evaluation we predominantly used:
> Confusion matrix
<img src="/Documentation/Konfusionsmatrix.png" height=350>

> Piechart
<img src="/Documentation/Kreisdiagramm.png" height=350>

### Overview
The basic components of our Application are divided into a php-server with database and a local python-Bottle-server.
The php-server manages the storage and acces to all saved repositories and a large part of preprocessing new ones.
To be independent of operating systems and further complications we decided to present all graphic elements in the browser with HTML.
As most machine-learning algorithms are too complex to implement them by ourselves without spending an extraordinary effort,
we relied on pre-existing libraries. The easiest access to such is available with Python so we chose it as our main backend language.

Specific requirements and information about installation: **Installation Manual.md**

### Python application
An explanation of our User-Interface with all functionas can be found in **Frontend Manual.md**.
Design of framework: **Active Learning Framework Planning Phase.md**


### Webserver
The server provides access to all collected data samples with additional filters and count-functionalities.
For more detailled information see **API.md**.

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
This all was implemented using the *Tfidf-Vectorizer* from the sklearn-package.

> **Word embeddings:** An alternative approach is to not represent a document as a vector accounting for all used words 
but to represent each word as vector which holds information about the context of it. 
So we end up with a matrix where each row stands for such a wordrepresenation. This embedding is learned through algorithms 
like presented in [this paper](https://papers.nips.cc/paper/5021-distributed-representations-of-words-and-phrases-and-their-compositionality.pdf).
A so called __Word2Vec__ model pretrained on Google-News articles which has a vocabulary size of 3 million distinct words is being used herefore.
Each word-vector is fed into a recurrent neural network (explained later) one after another.

> **Character by character:**
But instead of learning such a complex representation for each word we can just directly feed a text character-wise into such a network.
This method came in handy when trying to classify depending on features like the repository-name.
In many cases the name was too specific and complex to have ever appeared before and so no vector-representation is available with previous methods.  

 > **Edit distance:**
 When trying to classify repositories that belong to Homework, Documents or Education it's important to know how similar the names of files or folders are.
 Such repositories often contain folders like __Week 1, Week 2, Week 3, ...__. So to hand that information directly to our classifiers 
 we measured the average __Levenshtein distance__  of all files and folders.


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
* **Commit messages:** We considered them to not obtain enough valuable information to sacrifice both the increase in input-dimension for the classifiers 
and necessary api-calls.
* **Commit count**: Weren't used as we didn't measure any correlation with specific classes.



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

#### Possible features for the future
* **Count of filenames with min. Lev-Distanz**: Could be more informative for classes like __HW__ or __DOCS__ than the average Levenshtein distance and might be implemented in the future. 
* **Document vector:**
A possible approach similar to word embeddings is often refered to as __Doc2Vec__, presented [in this paper](https://cs.stanford.edu/~quocle/paragraph_vector.pdf).
While we weren't able to test this approach yet we're excited to see how it will compete against our current methods.


### Prediction Model

#### Neural networks
##### Feed-forward
Text
##### LSTM
Text

#### SVM
Test

#### ...


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

We consider a higher precision to be more relevant than a high recall per class. When thinking about a user, looking for repositories of a specific
class on GitHub, it appears way more desirable if the repositories proposed by us are actually of the right class.
Making sure every *DEV*-repository is presented to the user, potentially including wrongly as *DEV* labeled repositores didn't seem like the right approach.
As the precision per class goes up during training, the recall will do so automatically as well.
Emphasising precision while not neglecting recall completely we agreed upon Fscore as our metric.
With it it's possible to combine both values into one while being able to favor one over another.
