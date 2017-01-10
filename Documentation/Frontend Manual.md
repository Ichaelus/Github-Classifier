# Frontend Manual

The User Interface is designed to serve both for training and testing purposes. To keep them sepearated there are four different modi that can be selected in the header, each with its own behaviour.

## Modi Overview
1. Stream Based Active Learning 
2. Pool Based Active Learning
3. Test All Classifiers
4. Handle User Input

### 1. Stream Based Active Learning
<img src="Documentation/StreamBasedAL.jpg" height=300 alt="Image Stream Based Active Learing">

Selecting this or one of the other **AL** modis will display three buttons on the left side of the header. They are used to control the stream of input repositories. If you are done classifying repositories, either press the `pause` button or simply switch mode.

**Stream Based Active Learning** means that a random sample out of our pool of unlabeled data is being selected and classified by every classification module in the list. If one or more modules are uncertain about their output, you will be asked to classify the sample by your own. Otherwise the sample will be skipped.
Manual classified samples will then be transfered to the labeled pool of training samples that are used to increase the classifier precision. Skipped samples could be transfered to the semi-supervised training pool, though we decided to disable this feature because of its current negative outcome.

In order to calculate their uncertainty, the classifiers are using the selected uncertainty formula.

### 2. Pool Based Active Learning
<img src="Documentation/PoolBasedAL.jpg" height=300>

This variation works similar to Stream Based AI: it picks in turn a single classifier (marked in blue) which determines the sample with the highest uncertainty out of a random partition of the unlabed sample pool. Because of its nature of choosing the most uncertain sample, it will always ask for user classification.

### 3. Test All Classifiers
<img src="Documentation/Test.jpg" height=150>

Here you can refresh the statistics as well as a shortcut for retraining and saving all classifiers.
'Test classifiers' lets all classifiers categorize a pool of testdata given by Informaticup 2017 
(but labeled according to your classification rules) for calculating how accurate every works,
 thus it is shown with confusion matrix and accuracy per class.
'Extended Test Set' is a bigger pool of testdata selected from us 
and can be used for testing if you activate the checkbox.
You will find more information about the testing- and train-pool under the section 'Statistics'.

### 4. Handle User Input
<img src="Documentation/UserInput.jpg" height=250>
&nbsp;



