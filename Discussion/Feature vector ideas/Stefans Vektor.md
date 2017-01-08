# Stefans Vector Proposition

Note: Copied Andreas´ proposition for own convenience since his version also includes everything Michis has

>Note: Vectors can be either combined or seperate classifiers get used for different classifiers -> Ensemble Learning
>Each classifier-vector combo outputs presumed probability for each class (log-prob or softmax function for normalization)
>
>## Text Vectors (Short description, Readme and Name)
>* Bag of words with Tfidf-Vectorizer (Possible limitation to 2000-5000 most frequent Words max)
>* Doc2Vec -> Unsupervised/ Supervised training on as many repos as possible (Implementation to be uploadeds as soon as possible)
>* Example: [0.2, 0.1, 0.0, 2, ...]
>
>## Used languages
>* Binary decision if language is being used in repository
>* Example: ['CSS':1, 'Javascript':1, 'Java':0, ...] (Of course implemented without keys)
>
>## Numerical values
>* Note: Almost all these values have to be normalized between 0.0 - 1.0
>* TODO: Get best maximum for each value
>* forks
>* watchers
>* stargazers_count
>* open issues
>* subscribers_count
>* Maximum project depth
>* Commits
>* Contributors
>* Branches
>* Avg. number of words per commit
>* is_fork (in api: fork)
>* Maybe: Permissions (admin, push, pull true or false (0 or 1) each)
>* has_wiki (0 or 1)
>* has_downloads (0 or 1)

* We could compare different commits, e.g. ratio of commits of the persons with the most and 2nd most contributions, average number of commits or stuff
  like that
* We could also try to get some information about in what amount of time the majority of the work on a projekt was done,
  was the work distributed over several month? was there a single acitivity spike? Don´t know how easy it is to get that kind
  of information though (maybe number of months where works was done; some ratio (number of commits in most active month/total number of commits))
* Informations about author: is it a group of people or a person? How many repos/stars/followers does the person have? If it´s a group: 
  how many members does it have?
* Some projects have their license in the commit, branches etc bar, e.g. https://github.com/Microsoft/microsoft.github.io in cases like that it could be easy to use that information
* number of Pull requests (open/closed)
* Number of Releases
* Number of files total
* during the time where work was done on the project, how many month passed without a commit? 
* not only open issues, but also closed ones
* anzahl der ordner in einem repo; ratio ordner zu dateien