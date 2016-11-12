# Andis Vector Proposition
Note: Vectors can be either combined or seperate classifiers get used for different classifiers -> Ensemble Learning
Each classifier-vector combo outputs presumed probability for each class (log-prob or softmax function for normalization)

## Text Vectors (Short description, Readme and Name)
* Bag of words with Tfidf-Vectorizer (Possible limitation to 2000-5000 most frequent Words max)
* Doc2Vec -> Unsupervised/ Supervised training on as many repos as possible (Implementation to be uploadeds as soon as possible)
* Example: [0.2, 0.1, 0.0, 2, ...]

## Used languages
* Binary decision if language is being used in repository
* Example: ['CSS':1, 'Javascript':1, 'Java':0, ...] (Of course implemented without keys)

## Numerical values
* Note: Almost all these values have to be normalized between 0.0 - 1.0
* TODO: Get best maximum for each value
* forks
* watchers
* stargazers_count
* open issues
* subscribers_count
* Maximum project depth
* Commits
* Contributors
* Branches
* Avg. number of words per commit
* is_fork (in api: fork)
* Maybe: Permissions (admin, push, pull true or false (0 or 1) each)
* has_wiki (0 or 1)
* has_downloads (0 or 1)
