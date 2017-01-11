# GitHub Classifier

_Note: Open [UserManual.html](UserManual.html) for a better Markdown representation._


## Introduction

Welcome to the InformatiCup 2017 submission from the team of the **University of Augsburg**.

Over the last couple of months, we tried to develop an easy to use and - wherever applicable - generalised tool for both training and testing purposes of classification tasks. In the early stages, we had to decide where to put most of our efforts in and what to aim for. Thus, we would like to introduce you to our aims before letting you dive into our visualisations and results.

## Classification Goals and Restrictions

TODO

You can read further about our goals in **Documentation/Documentation.md**

## Component Correlation

Because of the need of a shared information base and the dependency on the [GitHub API](https://developer.github.com/v3/), we decided to encapsulate a few main concepts and connect them through few well defined interfaces. This leaves us basically with a remote backend system and multiple client applications.

<img src="/Documentation/component_correlation.png">

### The Backend

Whenever we gather information for a repository, about 10-100 of GitHub's `API-calls` (limited to 5000) are being used. In order to get along with this limitation we decided to set up an isolated remote [LAMP](https://en.wikipedia.org/wiki/LAMP_(software_bundle)) server which is able to _mine_ and store random repositories in a dedicated `MySQL database`. This gives us the freedom to work on and extend the same information base while running different clients in separated networks. More about the database structure and PHP services can be read in **Documentation/API.md**.

### The Client Application

The software actually containing the classification modules, feature extraction and GUI representation is located inside the  `./Application` folder and can be run OS-independent on your local machine. It is designed following the [MVC](https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller) pattern with Python running the heartbeat and [Bottle](https://en.wikipedia.org/wiki/Bottle_(web_framework)) offering services and files to the Frontend. The best of all: New classifiers can be easily embedded into the system just by being added to `Models/ClassificationModules`.

The frontend is where all the fun starts, so don't hesitate following the Installation Guideline - there is an introduction to the GUI as well in **Documentation/Frontend Manual.md**.

### Client Installation

Please select **Documentation/Installation Manual.md** on top of the page to get the Frontend running.