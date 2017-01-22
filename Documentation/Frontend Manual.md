# Frontend Manual

The User Interface is designed to serve both for training and testing purposes. To keep them separated there are four different modes that can be selected in the header, each with its own behaviour.

## The header - Mode Overview

1. Stream Based Active Learning 
2. Pool Based Active Learning
3. Test All Classifiers
4. Handle User Input

### 1. Stream Based Active Learning
<img src="/Documentation/StreamBasedAL.jpg" height=300 alt="Image Stream Based Active Learing">

Selecting this or one of the other **AL** modes will display three buttons on the left side of the header. They are used to control the stream of input repositories. If you are done classifying repositories, either press the `pause` button or simply switch mode.

**Stream Based Active Learning** means that a random sample out of our pool of unlabeled data is being selected and classified by every classification module in the list. If one or more modules are uncertain about their output, you will be asked to classify the sample on your own. Otherwise the sample will be skipped.
Manually classified samples will then be transferred to the labeled pool of training samples that are used to increase the classifier precision. Skipped samples could be transferred to the semi-supervised training pool, though we decided to disable this feature because of the current precision level.

In order to calculate their uncertainty, classifiers are using the selected uncertainty formula.

### 2. Pool Based Active Learning
<img src="/Documentation/PoolBasedAL.jpg" height=300>

This variation works similar to Stream Based AI: it picks in turn a single classifier (marked in blue) which determines the sample with the highest uncertainty out of a random partition of the unlabeled sample pool. Because of its nature of choosing the most uncertain sample, user classification will always be asked for the displayed sample.

### 3. Test All Classifiers
<img src="/Documentation/Control_Test.png" height=150>

The testing mode has been designed to manage and analyse classification modules. This includes operations and visualisations regarding their train state, save files and measurable outcome.

`Retrain all classifiers` will reset every (or every untrained) classifier and trains them on the current train set. Note that this will take a lot of time for modules that use high-dimensional features. `Save all classifiers` saves a copy of every module state to the disk.

If `Use extended test set` is disabled, test results are based on the [Appendix B](https://informaticup.github.io/InformatiCup2017/appendix-b-repositories), which has been pre-classified by our own classification criteria. When enabled, a more representative test set of about 300 samples is being used to calculate test results.

The button `Test classifiers` will bring the test results up to date if the checkbox above has changed. Note that you don't need to test classification modules manually in any other case.

In order to get a rough idea about the train/test set sample class distribution and per-table or rather per-attribute statistics, just hit the button `Statistics`.

### 4. Handle User Input
<img src="/Documentation/Control_HandleUserInput.png" height=150>

At times it might be interesting to test the classification modules on one or more non-random self-chosen repositories. If you are interested in the classification only, select the radio button `Always show prediction`. If you want to train the classifiers on your manual classification, chose `Always require user feedback`.

Clicking on `Predict single` will ask you to insert the link of a repository. It will then fetch information about that given repository from the server and calculate classifier results that are being shown to the user. Even entire lists of repository URLs can be processed by clicking the button `Predict list`.

## Main Sections

_The page is divided into a header, footer and main section. Depending on the actions performed in the control header, the main section (which always consists of an input, the classification modules and an output) changes its scope and contents._

### Input

<img src="/Documentation/Section_Input.png" height=350>

If any **A**ctive **L**earning or user input mode has been selected, the input will show a brief overview about the currently processed sample. Note that the attributes displayed to not comply with the features used by our classifiers.

<img src="/Documentation/Section_Test_Input.png" height=350>

In the `test mode`, a class distribution of the selected test set will be displayed. The test set can be changed inside the header section.  
  
### Classifiers and Classification Results

This section is basically an ordered list of classification modules (defined in `/Application/Modules/ClassificationModules`). The green little box consists of the module name, the value of the selected measure, and two actions:

<img src="/Documentation/Section_Main.png" height=350>

* `Show details` will open a wrapper containing deep insights in that classifier
* `Disable classifier` prevents this classifier to be asked for an output

Next to the green box, an arrow `=>` points to a matrix of float values. Those values represent either the precision per class (if you are inside the `test` mode) or the output probability the corresponding module would label the input sample as part of the given class. Green or red values over the arrow `=>` are pointing out whether the classifier is sure about its prediction or not.

The `detailed page` comes along with a few additional actions and analysis information:

<img src="/Documentation/Section_Detailed_Main.png" height=350>

* The **Performance Graph** is visualising the precision per class in a typical radar chart - different versions are overlapping to spot precision changes.
* New **versions** of that classifier can be created by hitting the button `Save current image`. To load an old image, chose the proper version and click `Load version`. The old version will be retested instantly on the selected test set.
* A **confusion matrix** lists precision and recall in absolute and normalized values
* The **measure table** lists the outcome values of this classifier for every predefined measure.

### Output

<img src="/Documentation/Section_Output.png" height=350>

Once again, the output changes whether or not the `test mode` is being selected. If it's not, the output gives you a brief overview about how the top-ranked classifier labels the selected input sample along with a list of how other modules would have guessed. Depending on your settings, an orange button labeled with **'?'** shows up if one or more classifiers are unsure about their output. Clicking on that button opens a new tab or window with more detailed repository information and the possibility to assign your personal classification label to that repository. 

<img src="/Documentation/Section_Test_Output.png" height=350>

The `test` output on the hand is non-interactive, its purpose is to present a summary about the top most listed classifier. Note that even if this may change depending on the measure selected in the central section, only the classifier selected in `Preordered` should be considered as our submission classifier.

## The Footer

You can find a link to the competition website at the very bottom of the GUI along with the names of every team member. Clicking on one of us will display a wrapper containing some information about him.