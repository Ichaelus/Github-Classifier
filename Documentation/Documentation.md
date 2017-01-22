# Documentation

1. First Insights
2. Software Architecture
3. Features and Prediction Model
4. Validation
5. Conclusion

## First Insights

### Confusion with class definitions
One of the biggest challenges was the unclear class definitions. We spent a lot of time discussing how to classify different
samples, there were many samples where different classes would have been a reasonable fit. We tried to extend the class definitions
on our own while trying to avoid conflicts with the sample repos and the short definitions in the challenge descriptions. 
We decided we wanted to classify the samples in a logical, consistent and somewhat intuitive way, even though some things
are debatable, e.g. WEB was defined as static personal websites and blogs. But when is a website non-static? As soon as there´s
some JavaScript or PHP involved? And is *personal websites only* a reasonable definition? Or shouldn´t a small, static website of some
sports team also be classified as a WEB sample?
Because of that we expect the results of the different teams to be very diverse and hard to compare. 
What we want to emphasize in the beginning: we didn´t take shortcuts and also deliberately chose to not make our lifes easy, e.g.
it would have been possible to just put every website that´s not a huge web app into WEB instead of trying to differentiate
like the given class definitions suggest. Doing that would have led to a huge increase in the precision of our classifiers
in the WEB class and other classes made us make similar decisions.

### Intelligent Sample Collection
Probably the most important sources of information about a GitHub repository is the readme and the short description text. 
As we knew we had to use them, we knew to achieve really good results we would need an extreme amount of samples, as text is 
a very hard to use feature for a classifier. Using word counts as example we knew we would get an input vector
with a dimension of several thousand. So for a classifier to actually learn the importance of each value of the input
vector, we would probably need at least ten thousands samples, and that´s not even counting in the majority class problem - 
repos belonging into the *DEV* category outnumber the repos of other categories by a large factor. As the repositories 
are really difficult to classify cleanly and consistently and because classification is really time consuming in this
particular scenario, we set ourselves the goal to try to utilize several different techniques to 
achieve a good result with a much smaller amount of samples.
The main method we used for that was **Active Learning**. We also tried different methods, like manually selecting repositories,
(for that, it was really important to choose them as diverse as possible) of different subclasses of the different classes,
as example the tutorial-repository subclass of the *EDU* class, and use them to get a jumpstart on the different categories. 
Later, when our classifier got better, we also tried to only classify samples where our best classifiers were
confident that it was neither a *DEV* nor *OTHER* repo, as these classes are much less interesting then the other ones.
By utilizing methods like these we are pretty happy with the performance we reached with only around 2000 samples.

### We built ourselves a somewhat reusable tool to help us with machine learning tasks like the given one
Experimenting with different features, classifiers and parameters can take a huge amount of time. So we designed and implemented
a tool that allowed us to use different classifiers like a black box, to save and load them and to test and analyse and compare
their performance. To make experimenting with different features possible, we didn´t only save the features we ended up using
in the end in our database, but saved all the information we thought could be useful in our database, so each classifier
could independently choose and process the features for itself.

### Classification Strategy
Being inspired by machine learning competitions like *Kaggle* or the *Netflix Prize*  we learned that 
almost every winning solution for most challenges there consists of combinations of various classifiers, also known as *Ensemble Learning*.
So we knew that we would somehow end up incorporating this technique right from the start. 
Eventually it ended up increasing the quality of our classifications drastically thus confirming our previous assumption.
In addition to that we wanted to try several state of the art algorithms and neural net architectures like *Word2Vec* or *LSTMs*.


### Our Strategy to get our train data
**Zeug aus diesem Absatz gegenchecken zu 1. Absatz**
As we approached this problem from a machine learning perspective we knew from the start that our models require a 
large and diverse collection of manually classified examples. We immediately decided we needed a tool
to help us building up a large collection of training samples. So, in order to speed up this process and make it
as pleasant as possible, we first set up a website whose aim was to display all necessary information about a repository
and to make it easy to classify the samples, the resulting data got saved to a database server.
GitHub only grants a limited number of API-calls available in a short amount of time so early on we stored
all hand-classified repositories with extracted features in a database to access them without restrictions.
In this process we filtered out all information (features) we needed and also possibly lacked to do so confidently.
Pretty soon we were surprised by how different our perspectives were in regards to which class to assign to many repositories.
For some thoughts on this at this time see *Discussions/List of corner cases.md*.
Following this we decided to abolish all samples we classified through weeks and start from the beginning.
The danger this diversity proposed to our classification-results was unacceptable.
So we worked out precise definitions of each class and listed vital edge cases.
The focus hereby laid on understandable definitions, finally sacrificing better evaluation scores of our models since 
many important distinctions are very hard 'to get' for these models.
After we learned from our mistakes we started to only classify in groups, later on handing this task over to only two team members
and finally to only one person as it became too time-consuming. 
Finally this person is responsible for more than 3/4 of all samples we use now. This way we maximized constistency and efficiency
without compiling a list of every single corner case to prevent ambiguity. 
Altough keeping this list updated would be nice to have, especially for outsiders, it has proven to be impossible
to do so without sacrificing an immense amount of time (and therefore collecting only half the samples we have now).
This problem arose with *Classification Ambiguities.md* and *List of corner cases.md* in the *Discussions* folder.
Mistakes made by this one person couldn't be prevented but eliminating the possibility of confusing differences in proposed classifications
was our priority.
Using this method we finally classified over 2000 repositories by hand.


### First Data Set Impressions

After building up our first set of training-data we were confronted with a serious problem:
We encountered a so called Majority Class Problem. As GitHub is mainly used for software development projects the class
**Development (DEV)** appeared way more frequently as any other class, taking up around 80% of all public repositories on GitHub. **Better %?**
This resulted in our first classifiers assigning *DEV* to almost every repository as it was right  doing so most of the time.
Our first approach to this problem was to split up the prediction process into a first step where only the distinction between *DEV* and *NOT Dev* 
has to been made. If it was classified as *NOT Dev* we'd show the repository to a classifier which only knew how to classify such 
(see classification-skizze.png for more).
We dropped this technique later on as we started to weight the importance of each sample during training with respect to the frequency of it's class.

Furthermore we incorporated the use of *Active Learning* in our training process 
([click here for more information](https://goo.gl/TPWjGo)).
By this we were able to only present such repositories to us for manual classification which our classifiers were particularly unsure about.
We used this approach to improve our classifiers more effectively by not hand-classifying redundant repositories.
This was achieved by maintaining a large pool (~35,000) of unlabeled repositories in our database.
Two modes were implemented:
* *Stream based* One random repository from the pool is selected and shown to the classifiers. If a classifier is unsure about the class, 
the user (like an Oracle) is being questioned.
* *Pool based* In turns each classifier is shown a subset of these repositories and picks the one it's most uncertain about for further questioning.  
To measure the uncertainty about a sample, various formulas are provided.
Our experience with this method was very positive although it turned out to not solve the issue of training altogether.
The repositories presented to the user were almost exclusively edge-cases.
On the one hand that was beneficial but in order for most of our classifiers to work correctly we needed a 
large amount of samples with clear and easy to interpret features to confirm assumptions about correlation between features.
We partly tackled this problem by adjusting the parameters which determine when a classification is assumed to be confident/unsure.

### Class Descriptions
As we didn't consider the class descriptions to be precise we added further explanations and
also partially changed the pre-existing ones, later we decided we have too many new
border cases all the time so a single team member took over all the classifying at some point
to save the extreme amount of time we spent discussing samples and trying to keep our classifications
consistent.
(To examine our old extended class descriptions and explanation of edge cases see **Classification Ambiguities.md**)


## Software Architecture
### Motivation
As we already tried several different classification methods and spent a lot of time iterating and 
trying to understand how to use each other's code we decided we needed a tool that allowed us to use
different classifiers as black box and to analyse their performance independent of the inner 
workings. ...

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

> Different measures
<img src="/Documentation/measures.png" height=350>

### Overview
<img src="/Documentation/component_correlation.png">
The basic components of our Application are divided into a PHP-server with a dedicated database connection and a local Python-Bottle-server.
The PHP-server manages the storage and access to all saved repositories and a large part of generating and pre-processing them.
To be independent of operating systems and further complications we decided to present all graphic elements in the client browser using HTML.
As most machine-learning algorithms are too complex to implement them by ourselves without spending an extraordinary time effort,
we relied on pre-existing libraries. The easiest access to such is available with Python so we chose it as our main backend language.

Specific requirements and information about the installation can be found in: **Installation Manual.md**

### Python application
Design of framework: **Active Learning Framework Planning Phase.md**  

The main functionality is split up in 5 core components:
First being *DatabaseCommunication.py* which handles all access to our database.
This way we can - for example - download all our training data by just calling a single function.
The returned samples/repositories provide all features available, it's now up to the classifier to filter out the features it needs.
This happens in *FeatureProcessing.py*. The extraction and pre-processing of a sample's features happens here.  
Formatting and processing for I/O and presentation is done in *JSONCommunication.py*. Here we turn classifier results into confusion matrices and create XML-files for saved classifiers. 
The management of all classifiers currently presented is the goal of *ClassifierCollection.py*. At the start of the application we load all used classifiers in this collection and so if we want to train, test, save and generally use them, we just need to call the methods of this specific class.
The interchangeability of these classifiers is guaranteed by creating the abstract class *ClassificationModules.py*.
You will find more information about them later under *Prediction Model*.

### User Interface
An explanation of our User-Interface with all functions can be found in **Frontend Manual.md**.

In order to keep the Frontend highly dynamic even with time-intensive user requests such as _train a classifier_ we decided to use the JavaScript library [VueJS](http://vuejs.org/) in order to bind certain 'states' to the HTML DOM tree. This results in a quite large _index.html_ file which represents every possible GUI states that are being styled by _overview.css_. Reactivity and observation is being brought to it by the file _frontend.js_, which also has a connection to the Python Controller *HomeController.py*. To sum up this nested relationship of different files: JavaScript tries to satisfy user wishes by updating the internal view state via Python services.

### Webserver

The _Webserver_ is basically a PHP server running the file contents of the folder **Backend**. Its main file _ajax.php_ provides a bunch of services such as access to all collected data samples with additional filters and count-functionalities. In order to store and fetch those samples, it is connected to a MySQL database via _mysqli_class.php_. _Ajax.php_ is also the only file that has access to the GitHub API via the controller _GitHandler.class.php_ - this is why the server can be used to _mine_ random repository samples and store extracted data to the database in order not to being limited to GitHub's API in production.

More detailed information about its services and more can be found in **API.md**.

## Features and Prediction Model
### Features

#### Implementation Details
All classifiers have access to the features of a repository by using the functions provided in *FeatureProcessing.py*.
They can request the features for a repository by calling the specific functions like *getMetadataVector* or *getReadme*.

#### Feature Development
To create the optimal feature vector every team member compiled a list of possible features (see Discussion/Feature Vector Ideas).
We then discussed every proposal and added further ones.
It's notable that the features considered most important by us at first where almost exclusively text based.
Readme, description, folder names, file names, author name and more. Unfortunately we had to limit the access of our models to 
the folder and filenames of only the first layer in a repository's folder-structure. This was due to the previously mention API-Call limit.
"In Diskussionen einigten wir uns auch der Verlockung durch festgelegte
Schlüsselwörter zu widerstehen, Mustererkennung sollte dem Klassifizierer überlassen bleiben." # Soll das hier rein?
In these discussion we discovered many features we first neglected: used programming languages (with a possible emphasis on the main language),
depth of the folder-structure, commit count, average commit-length, branch count, whether a download of the repository is allowed, folder-count,
number of files and more. Later we additionally implemented the average Levenshtein distance between folder and filenames. This was done
due to a lack of any feature that can give us valuable information despite the fact that many DOCS or HW folder-/filenames are often similar.

#### Text
> **Frequency-based methods:** We count the frequency of specific tokens or words in our documents and 
therefore encode the text in a sparse vector with each element representing how often one specific word/token occurs (large number = high frequency).
Using this approach we had to consider how long this vector may be in order to be as efficient as possible.
We only count the frequency of the __x__ most frequent terms (excluding stop-words). 
While short vectors (and therefore less words we can keep track of) allow more robust classification
results for our classifiers, we may lose important information that could make important distinctions (such as HW vs EDU) impossible.
Having this problem in mind we also used a trick to reduce the necessary dimensionality a lot by not encoding each word 
but the word stem ('library' and 'libraries' are bot represented by '__librari__').
The resulting number of necessary words/tokens turned out to differ from the text we encoded. 
We use smaller numbers (~2000) for repository-descriptions and even less (~200) for folder-/filenames.
The readme turned out to need a lot more (~6000).
This all was implemented using the *Tfidf-Vectorizer* from the sklearn-package.

> **Word embedding:** An alternative approach is to not represent a document as a vector accounting for all used words 
but to represent each word as vector which holds information about the context of it. 
So we end up with a matrix where each row stands for such a word representation. This embedding is learned through algorithms 
like presented in [this paper](https://papers.nips.cc/paper/5021-distributed-representations-of-words-and-phrases-and-their-compositionality.pdf).
A so called __Word2Vec__ model pre-trained on Google-News articles which has a vocabulary size of 3 million distinct words is being used here for.
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

#### Numerical features

#### Metadata:
* **hasDownload**: Boolean value if repository can be downloaded directly.
* **watches**: Count of people who follow latest news in respect to new pull requests and issues that are created.
* **folder_count**: Count of folders is currently limited due to limited API-calls available.
* **treeDepth**: Depth of folder-structure. Also capped at the moment due to limited API-calls.
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
* **verwendete Sprachen**: Used programming languages (represented as vector with each column representing one language. 0.5 if language is being used, 1.0 if it's the repository's main language).

#### Dismissed features:
* **Commit messages:** We considered them to not obtain enough valuable information to sacrifice both the increase in input-dimension for the classifiers 
and necessary API-calls.
* **Commit count**: Weren't used as we didn't measure any correlation with specific classes.

#### Possible features for the future
* **Count of filenames with min. Lev-distance**: Could be more informative for classes like __HW__ or __DOCS__ than the average Levenshtein distance and might be implemented in the future. 
* **Document vector:**
A possible approach similar to word embedding is often referred to as __Doc2Vec__, presented [in this paper](https://cs.stanford.edu/~quocle/paragraph_vector.pdf).
While we weren't able to test this approach yet we're excited to see how it will compete against our current methods.

### Prediction Model

#### Implementation Details
We wrote a lot about the desired interchangeability and modularity of our models in order to train, evaluate and compare them as efficient as possible.
This was achieved through the following design:
Classifiers are represented by an abstract class called **ClassificationModule** (*ClassificationModule.py*), Ensemble Classifiers
are classes which inherit the class **EnsembleClassifier** (*EnsembleCLassifier.py*) which just adds a small amount of functionality to the ClassificationModule.
Through that we got a unified interface for our classifiers and each Model is represented by a class which just
has to implement the abstract methods from ClassificationModule like *train* or *predictLabelAndProbability*.

#### Used models
We hereby present all models used in the process, to look at our first tests see the **Playground** folder.

> **Neural Networks** are without any doubt the most hyped up machine learning models since many years. 
Mastering many difficult challenges [like finding the right category out of thousands for images](http://image-net.org/) at human like performance.
So we tried the most popular architectures to make use of this immense capability.
The first architecture we tried was a standard **feedforward** network.
Depending on the complexity of the feature-space we mostly used 2 or less layers, also trying 3 layers for frequency based feature-spaces.
When using more layers we quickly saw an immense loss in *generalization* and the network *overfitted* on the training data 
(meaning that it only memorized repositories and their right class instead of actually learning how to interpret the given features).
As activation function we favored the newer [*ReLU* or *Noisy ReLU*](https://en.wikipedia.org/wiki/Rectifier_(neural_networks)) over the previously used *tanh* and *sigmoid* functions [for various reasons](https://stats.stackexchange.com/questions/126238/what-are-the-advantages-of-relu-over-sigmoid-function-in-deep-neural-network).
As our *optimizer* we chose [*ADAM*](http://sebastianruder.com/optimizing-gradient-descent/index.html#adam) for this network-type.
Having these things in mind our networks performed pretty well, always being among the best classifiers.
The above mentioned **LSTM** networks came in handy when classifying based on a sequence of inputs (like characters or word-embedding).
By feeding their last activation to themselves, these neurons "remember" their previous inputs (like the last characters forming a sentence).
A helpful explanation can be found [here](https://colah.github.io/posts/2015-08-Understanding-LSTMs/).
For reasons like improving training time *Stochastic gradient descent* was used for training here.    
For the last layer of all networks consisted of a fully connected layer with an applied *softmax* function to output actual predictions.
To implement them we used the popular [Keras library](https://keras.io/) running on top of [Theano](https://github.com/Theano/Theano).

> **SVMs (Support Vector Machines)** were an obvious choice, having proven to be a robust method for both regression and classification problems.
After only a few tries we quickly decided to use the popular non-linear [*RBF-kernel*](https://en.wikipedia.org/wiki/Radial_basis_function_kernel) 
over the linear version. Using that we had to find the best combination of the [C and gamma](http://scikit-learn.org/stable/auto_examples/svm/plot_rbf_parameters.html) values.
We used them for all kinds of features, each time they've proven to be a serious competitor to our *neural networks*.
The used library was [Scikit-learn](http://scikit-learn.org/stable/).

> We considered **Naive Bayes** classifiers to be very promising for text classification as they are in many cases.
But even after trying out many [*event models*](https://en.wikipedia.org/wiki/Naive_Bayes_classifier#Parameter_estimation_and_event_models) the results were rarely satisfying.
After trying different combinations of lengths of the Frequency based features we omitted their further use.
Same for our [Nearest Neighbors classifiers](http://scikit-learn.org/stable/modules/neighbors.html), even though we also tried non-text features with them.
Both are contained in the [Scikit-learn library](http://scikit-learn.org/stable/).

> **Ensemble methods** combine the capabilities of various classifiers to make an even more powerful prediction.
The methods we used were incredibly powerful like the **Random Forests** or **Gradient Tree Boosting**. **AdaBoost** turned out to 
depend strongly on the used base-classifiers but after some tries our other methods outperformed them most of the time so we omitted further use.
All these were already implemented in the Scikit-learn library. Parameter tuning mostly depended on adjusting the number of base-classifiers.
They were not only often times the most robust classifiers but also outperformed *neural nets* or *SVMs* in many cases.
After reading [articles like this](http://mlwave.com/kaggle-ensembling-guide/) we began creating our final classifier used for the competition.
**Stacking** is a general term for combining only the predictions of other learning algorithms also often referred to as **Stacked Generalization**.
Among the great variety of methods we selected, implemented and finally compared three different methods:
One was to simply let the classifiers vote democratically by simply taking the **average** probability per class.
This made our classification way more robust and delivered an incredibly satisfying result.
The second method is the probably most famous one: We trained a **linear classifier** to let the classifiers vote on the class 
but not without assigning a weight to the predictions of each classifier. This way we wanted to enable the classifiers to mainly decide on the classes
they were best at. This was implemented using sklearn's **Linear Regression** class.
But the third was the one we actually used for our final model. Instead of just letting the meta-classifier learn, which base-classifier
delivered the best results for each class we supplied it with additional information about the repository.
This information consisted of a collection of hand-selected features: the count of folders, files and commits, 
the edit distance among the folder and filenames, the length of readme, the average length of each commit and finally the depth of the folder structure.
The reasoning behind this all was the following: The base-classifiers were not only different in terms of machine learning models but were
also trained on different features. We use on Neural Net (LSTM) which only has knowledge of the repository-name while one Support Vector Machines
has knowledge of all features except that name and so on. So the quality of each classifiers prediction varies from repository to repository.
We fed all this data, the predictions of our base-classifiers and in addition this subset of meta-features, in a neural network with one hidden layer.
This network is now able to not only tell which sub-classifier generally is most reliable when it comes to one class but knows
which classifier might be most reliable specifically for the current repository. When for example the readme-length is very
small or it's even empty the classifiers depending on the readme will not produce reliable predictions. But now it's able to recognize
that and watch out specifically what other classifiers like the repo-name LSTM predict.
This method allowed us to produce even more robust predictions, outperforming all previously mentioned ones.


## Validation
"Apply your classifier on the repositories included in  Appendix B . 
You can find this file on https://github.com/InformatiCup/InformatiCup2017 as well. 
Create a Boolean matrix where you compare the results where you compare the results of your 
classifier and your intuitive classification (if your intuitive classification matches the output 
of your program, the element in the matrix will result to true, otherwise to false).
Compute the recall per category- the number of repositories intuitively placed within a 
category in the set of repositories that got placed in the same category by your classifier.
Compute the  precision per category- the number of repositories per category where the results 
determined by your automatic classifier matched your intuitive classification."

<table>
	<thead>
		<tr>
			<th>Repository</th>
			<th>Manual classification</th>
			<th>Calculated class</th>
		</tr>
	</thead>
	<tbody>
	<tr>
	    <td>https://github.com/ga-chicago/wdi5-homework</td>
	    <td>HW</td>
	    <td>HW</td>
    </tr>
    <tr>
	    <td>https://github.com/Aggregates/MI_HW2</td>
	    <td>HW</td>
	    <td>DEV</td>
    </tr>
    <tr>
	    <td>https://github.com/datasciencelabs/2016/</td>
	    <td>EDU</td>
	    <td>EDU</td>
    </tr>
    <tr>
	    <td>https://github.com/githubteacher/intro-november-2015</td>
	    <td>EDU</td>
	    <td>EDU</td>
    </tr>
    <tr>
	    <td>https://github.com/atom/atom</td>
	    <td>DEV</td>
	    <td>DEV</td>
    </tr>
    <tr>
	    <td>https://github.com/jmcglone/jmcglone.github.io</td>
	    <td>WEB</td>
	    <td>WEB</td>
    </tr>
    <tr>
	    <td>https://github.com/hpi-swt2-exercise/java-tdd-challenge</td>
	    <td>HW</td>
	    <td>DEV</td>
    </tr>
    <tr>
	    <td>https://github.com/alphagov/performanceplatform-documentation</td>
	    <td>DOCS</td>
	    <td>DEV</td>
    </tr>
    <tr>
	    <td>https://github.com/harvesthq/how-to-walkabout</td>
	    <td>EDU</td>
	    <td>DEV</td>
    </tr>
    <tr>
	    <td>https://github.com/vhf/free-programming-books</td>
	    <td>EDU</td>
	    <td>EDU</td>
    </tr>
    <tr>
	    <td>https://github.com/d3/d3</td>
	    <td>DEV</td>
	    <td>DEV</td>
    </tr>
    <tr>
	    <td>https://github.com/carlosmn/CoMa-II</td>
	    <td>HW</td>
	    <td>DOCS</td>
    </tr>
    <tr>
	    <td>https://github.com/git/git-scm.com</td>
	    <td>DEV</td>
	    <td>DEV</td>
    </tr>
    <tr>
	    <td>https://github.com/PowerDNS/pdns</td>
	    <td>DEV</td>
	    <td>DEV</td>
    </tr>
    <tr>
	    <td>https://github.com/cmrberry/cs6300-git-practice</td>
	    <td>HW</td>
	    <td>DEV</td>
    </tr>
    <tr>
	    <td>https://github.com/Sefaria/Sefaria-Project</td>
	    <td>DEV</td>
	    <td>DEV</td>
    </tr>
    <tr>
	    <td>https://github.com/mongodb/docs</td>
	    <td>DOCS</td>
	    <td>DEV</td>
    </tr>
    <tr>
	    <td>https://github.com/sindresorhus/eslint-config-xo</td>
	    <td>DEV</td>
	    <td>DEV</td>
    </tr>
    <tr>
	    <td>https://github.com/e-books/backbone.en.douceur</td>
	    <td>EDU</td>
	    <td>EDU</td>
    </tr>
    <tr>
	    <td>https://github.com/erikflowers/weather-icons</td>
	    <td>DOCS</td>
	    <td>DEV</td>
    </tr>
    <tr>
	    <td>https://github.com/tensorflow/tensorflow</td>
	    <td>DEV</td>
	    <td>DEV</td>
    </tr>
    <tr>
	    <td>https://github.com/cs231n/cs231n.github.io</td>
	    <td>WEB</td>
	    <td>WEB</td>
    </tr>
    <tr>
	    <td>https://github.com/m2mtech/smashtag-2015</td>
	    <td>HW</td>
	    <td>HW</td>
    </tr>
    <tr>
	    <td>https://github.com/openaddresses/openaddresses</td>
	    <td>DATA</td>
	    <td>DATA</td>
    </tr>
    <tr>
	    <td>https://github.com/benbalter/congressional-districts</td>
	    <td>DATA</td>
	    <td>EDU</td>
    </tr>
    <tr>
	    <td>https://github.com/Chicago/food-inspections-evaluation</td>
	    <td>DEV</td>
	    <td>EDU</td>
    </tr>
    <tr>
	    <td>https://github.com/OpenInstitute/OpenDuka</td>
	    <td>DEV</td>
	    <td>DEV</td>
    </tr>
    <tr>
	    <td>https://github.com/torvalds/linux</td>
	    <td>DEV</td>
	    <td>DEV</td>
    </tr>
    <tr>
	    <td>https://github.com/bhuga/bhuga.net</td>
	    <td>WEB</td>
	    <td>DEV</td>
    </tr>
    <tr>
	    <td>https://github.com/macloo/just_enough_code</td>
	    <td>EDU</td>
	    <td>EDU</td>
    </tr>
    <tr>
	    <td>https://github.com/hughperkins/howto-jenkins-ssl</td>
	    <td>EDU</td>
	    <td>EDU</td>
    </tr>
	</tbody>
</table>

<table>
    <thead>
        <tr>
            <th>Class</th>
            <th>Precision obtained</th>
            <th>Recall obtained</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>DEV</strong></td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td><strong>HW</strong></td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td><strong>EDU</strong></td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td><strong>DOCS</strong></td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td><strong>WEB</strong></td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td><strong>DATA</strong></td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td><strong>OTHER</strong></td>
            <td></td>
            <td></td>
        </tr>
    </tbody>
</table>

> Confusion matrix, later to be replaced with the resulting confusion matrix of the final classifier when classifying Appendix_B Repos,
> maybe the table on top of this picture is redundant then?
<img src="/Documentation/Konfusionsmatrix.png" height=350>

### Example Repositories
"Please document three repositories where you assume that your 
application will yield better results as compared to the results of other teams."
Hinweise um solche bei uns zu finden:
* HW/DOC könnte durch Levenshtein distance besser sein...
* ??

### Precision vs Yield/ Recall
We consider a higher precision to be more relevant than a high recall per class. When thinking about a user, looking for repositories of a specific
class on GitHub, it appears way more desirable if the repositories proposed by us are actually of the right class.
Making sure every *DEV*-repository is presented to the user, potentially including wrongly as *DEV* labeled repositories didn't seem like the right approach.
As the precision per class goes up during training, the recall will do so automatically as well.
Emphasising precision while not neglecting recall completely we agreed upon Fscore as our metric.
With it it's possible to combine both values into one while being able to favour one over another.

## Conclusion
### Hard Problem
Text Classification isn´t easy and the different classes are extremely hard to distinguish.
So hard in fact, that even us as humans had problems agreeing on the class labels after classifying
hundreds and thousands of repos before. So, if we humans disagree on every second sample, we probably 
can´t expect our classifiers to perform a lot better that that, especially considering the extreme 
amount of information per repo.
### Features
Talk about information per repo we used and didn´t use here. **Nein, das haben wir doch oben schon genau gemacht?**
Word counts aren´t that good and we tried our luck with LSTMS.
We had our reasons for not using the commits.
File contents are utopic and impossible to use in this situation.
So we used/tried using everything or had a good reason for not using it. 
### Our classifiers clearly reached a ceiling
No classifier performed much better than 60% precision M, no matter how much parameter tuning, but we reached a value 
near that with several different classifiers, so that probably was some sort of limit how much can be achieved with our 
features and amount/cleanness of our train data. With an Ensemble classifier, just like in competitions like Kaggle, 
we somewhat managed to gain a few extra percent points.
### Interpretation of our results
60% x sounds like a pretty good number when we humans disagreed on what felt like every second sample.
While working on the given challenge, we learned a lot about machine learning, although unfortunately we couldn´t utilize 
every method we learnt about during the work on the project. 
However, we developed a framework that we will very likely use again the next time we get to work on a machine learning 
project. After building our application, the testing and comparison of different methods and parameters was incredible 
comfortable.