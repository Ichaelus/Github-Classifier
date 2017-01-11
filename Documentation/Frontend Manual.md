# Frontend Manual

The User Interface is designed to serve both for training and testing purposes. To keep them sepearated there are four different modi that can be selected in the header, each with its own behaviour.

## Modi Overview
1. Stream Based Active Learning 
2. Pool Based Active Learning
3. Test All Classifiers
4. Handle User Input

### 1. Stream Based Active Learning
<img src="/Documentation/StreamBasedAL.jpg" height=300 alt="Image Stream Based Active Learing">

Selecting this or one of the other **AL** modi will display three buttons on the left side of the header. They are used to control the stream of input repositories. If you are done classifying repositories, either press the `pause` button or simply switch mode.

**Stream Based Active Learning** means that a random sample out of our pool of unlabeled data is being selected and classified by every classification module in the list. If one or more modules are uncertain about their output, you will be asked to classify the sample by your own. Otherwise the sample will be skipped.
Manually classified samples will then be transfered to the labeled pool of training samples that are used to increase the classifier precision. Skipped samples could be transfered to the semi-supervised training pool, though we decided to disable this feature because of its current negative outcome.

In order to calculate their uncertainty, classifiers are using the selected uncertainty formula.

### 2. Pool Based Active Learning
<img src="/Documentation/PoolBasedAL.jpg" height=300>

This variation works similar to Stream Based AI: it picks in turn a single classifier (marked in blue) which determines the sample with the highest uncertainty out of a random partition of the unlabed sample pool. Because of its nature of choosing the most uncertain sample, user classification will always be asked for the displayed sample.

### 3. Test All Classifiers
<img src="/Documentation/Control_Test.png" height=150>

The testing mode has been designed to manage and analyze classification modules. This includes operations and visualisations regarding their train state, savefiles and measurable outcome.

`Retrain all classifiers` will reset every (or every untrained) classifier and trains them on the current train set. Note that this will take a lot of time for modules that use large features. `Save all classifiers` saves a copy of every module state to the disk.

If `Use extended test set` is disabled, test results are based on the [Appendix B](https://informaticup.github.io/InformatiCup2017/appendix-b-repositories), which has been preclassified by our own classification criterias. When enabled, a more representative testset of about 300 samples is being used to calculate test results.

The button `Test classifiers` will bring the test results up to date if the checkbox above has changed. Note that you don't need to test classification modules manually in any other case.

In order to get a rough idea about the train/test set sample class distribution and per-table or rather per-attribute statistics, just hit the button `Statistics`.

### 4. Handle User Input
<img src="/Documentation/Control_HandleUserInput.png" height=150>

At times it might be interesting to test the classification modules on one or more non-random self chosen repositories. If you are interested in the classification only, select the radio button `Always show prediction`. If you want to train the classifiers on your manual classification, chose `Always require user feedback`.

Clicking on `Predict single` will ask you to insert the link a repository. It will then fetch information about that given repository from the server and calculate classifier results that are being shown to the user. Even entire lists of repository URLs can be processed by clicking the button `Predict list`.

## Sections

### Input

### Classifiers

### Output

TODO