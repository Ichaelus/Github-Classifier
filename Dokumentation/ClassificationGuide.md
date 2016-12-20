# Classification Guidelines


## DEV
> A repository primarily used for development of a tool, component, application, app, or API

#### Examples
* [A simple rails app to handle homework assignment submission and grading](https://github.com/briantemple/homeworkr)
* [Spring Boot makes it easy to create Spring-powered, production-grade applications and services with absolute minimum fuss](https://github.com/spring-projects/spring-boot)
* [A declarative, efficient, and flexible JavaScript library for building user interfaces](https://github.com/facebook/react)
* [Native Node bindings to Git.](https://github.com/nodegit/nodegit)
* [Scipy library main repository.](https://github.com/scipy/scipy)


## HW
> A repository primarily used for homework, assignments and other course-related work and code

#### Examples
* [CodePath week 1 homework](https://github.com/spez/RottenTomatoes)
* [Calculator of the cs193p lecture](https://github.com/m2mtech/calculator-2015)
* [Class github repository for 751 and 2; doctoral classes in the Department of Biostatistics at Johns Hopkins ](https://github.com/bcaffo/751and2)
* [PrettyPrettyPrint](https://github.com/HPI-SWA-Teaching/SWT16-Project-08)
* [An example homework assignment using Python.](https://github.com/uwhpsc-2016/example-python-homework)


## EDU
> A repository primarily used to host tutorials, lectures, educational information and code related to teaching

#### Examples
* [ Course materials for the Data Science Specialization](https://github.com/DataScienceSpecialization/courses)
* [Introduction to GitHub (November 2015)](https://github.com/githubteacher/intro-november-2015)
* [An attempt to answer the age old interview question "What happens when you type google.com into your browser and press enter?"](https://github.com/alex/what-happens-when)
* [Mostly adequate guide to FP (in javascript)](https://github.com/MostlyAdequate/mostly-adequate-guide)
* [A collection of tips to help up your jQuery game](https://github.com/AllThingsSmitty/jquery-tips-everyone-should-know)


## DOCS
> A repository primarily used for tracking and storage of non-educational documents

#### Examples
* [CMS Developer Site](https://github.com/CMSgov/HealthCare.gov-Styleguide)
* [A maturity model for adopting open source](https://github.com/github/maturity-model)
* [Official documentation for the Raspberry Pi](https://github.com/raspberrypi/documentation)
* [Bundesgesetze und -verordnungen](https://github.com/bundestag/gesetze)
* [_Dokumente der Fachschaft IT-Systems Engineering am Hasso-Plattner-Institut an der Universität Potsdam_](https://github.com/fsr-itse/docs)

## WEB
> A repository primarily used to host static personal websites or blogs

#### Examples
* [Paul Ford’s “What Is Code?”](https://github.com/BloombergMedia/whatiscode)
* [Webpage to display the results of data mining project of Twitter for class CS-3250-01 Computational Data Analysis taught by Dr. Doran at Wright State University. ](https://github.com/JaceRobinson8/jacerobinson8.github.io)
* [The website of Ruby Monstas Zurich](https://github.com/rubymonstas-zurich/rubymonstas-zurich.github.io)
* [Create an academic personal website on Jekyll and GitHub Pages](https://github.com/ianli/elbowpatched-boilerplate)
* [whoisjuan portfolio](https://github.com/whoisjuan/whoisjuan.github.io)

## DATA
> A repository primarily used to store data sets

#### Examples
* [San Francisco housing construction history and associated data ](https://github.com/ericfischer/housing-inventory)
* [Assorted data from the General Services Administration.](https://github.com/GSA/data)
* [The Open Exoplanet Catalogue](https://github.com/OpenExoplanetCatalogue/open_exoplanet_catalogue)
* [University Domains and Names Data List & API](https://github.com/Hipo/university-domains-list)
* [The Big List of Naughty Strings is a list of strings which have a high probability of causing issues when used as user-input data. ](https://github.com/minimaxir/big-list-of-naughty-strings)

## OTHER
> Use this category only if there is no strong correlation to any other repository
category, for example, empty repositories

#### Examples
* [TestEmptyRepository](https://github.com/libgit2/TestEmptyRepository)


## Ambiguities
> List possible confusions here if encountered while training...

#### Lecture repos
> Whenever the focus of such repo lays on homework assignments, 'HW' is the correct class. When focus lays primarily on hosting of documents, choose 'EDU'.

#### Design Principles or Standards
> Mostly belong to docs as they're non-educational. Be careful here and look out for occuring explanations (Obviously 'EDU' then).

#### Scripts and Functional Plugins
> If repo is used mainly for development and not for hosting, 'DEV' is the desired class. 'DOCS' get's used if not.  
> **Example:** [gmon-scripts](https://github.com/gwoo/gmon-scripts) was classified as 'DOCS'.

#### Empty repositories
> If repo is empty, 'OTHER' is the class to go with. Even if purpose of repo is obvious (e.g. repo-name is sth. like "XYZ.github.io").

#### DOCS vs DATA
> Look out for folder structure and filetypes ('.csv', ...)
> [language-tag-extensions](https://github.com/ppKrauss/language-tag-extensions) is 'DATA'

#### Websites
> Decision if Web or Dev depends on complexity of website.   
> **Note:** We changed the official class-description from only _personal_ 'static website' to **just** 'static website'. This constraint didn't seem plausible.

#### Collection of tips
> **Example:** 'Collection of Android tips' is educational so 'EDU' is the way to go.

#### Collection of problems vs answers to them
> Whereas answers to possible questions are of an educational origin, the sole collection of such should be seen as a collection.    
> In the first case choose 'EDU', 'DOCS' elsewhen.  

#### Dummy repositories
> If the focus of a repository lays on the existence of it only and not on storage of information (repository is _almost_ empty or doesnt contain any files), we call it a **Dummy** repository.  
> Even such repository is subject to practice or homework, 'OTHER' should be chosen nevertheless.  
> [This repo is for demonstration purposes only.](https://github.com/octocat/Spoon-Knife)

#### Data-Visualization
> If repo contains dataset and visualization as well, 'DATA' should still be chosen.    
> Altough this applies only to repositories, that contain such datasets. If datasets in general can be used for these programs, 'DEV' is the better choice.  

#### DOCS vs EDU
> A bug reproduction description that does not contain the solution (no educational value) -> DOCS
> **Example** [Bug description](https://api.github.com/repos/GrahamDennis/spark-kryo-serialisation)

#### DOCS vs DEV
> A repository containing a project structure always tends to be DEV. Only if the readme implies to be categorised as DOCS, it should be classified as such.
> A project primarily used for storing files, even if those files are code and get small changes, is still docs
> A **single commit** of a **fully developed** project tends to be rather DOCS than DEV.
> **Example** [Code stored for creating a tutorial](https://github.com/yahwin/backbone-tutorials)

### EDU vs HW
> Homework instructions and the work on some homework is HW. However, if only homework solutions are stored somewhere,
> along with other code for educational purposes it´s EDU? Did only encounter this a single time sofar, can still be changed.
> **Example** [Code related to an educational book, which also contains exercises] https://github.com/alakras/javaForTestersCode

#### Example / showcase projects
> EDU
