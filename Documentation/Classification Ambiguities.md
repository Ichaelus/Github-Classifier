# Classification Ambiguities

> List possible confusions here if encountered while training...

### Lecture repos
> Whenever the focus of such repo lays on homework assignments, 'HW' is the correct class. When focus lays primarily on hosting of documents, choose 'EDU'.

### Design Principles or Standards
> Mostly belong to docs as they're non-educational. Be careful here and look out for occurring explanations (Obviously 'EDU' then).

### Scripts and Functional Plugins
> If repo is used mainly for development and not for hosting, 'DEV' is the desired class. 'DOCS' gets used if not.  
> **Example:** [gmon-scripts](https://github.com/gwoo/gmon-scripts) was classified as 'DOCS'.

### Empty repositories
> If repo is empty, 'OTHER' is the class to go with. Even if purpose of repo is obvious (e.g. repo-name is sth. like "XYZ.github.io").

### DOCS vs DATA
> Look out for folder structure and file types ('.csv', ...)  
> **Example:** [language-tag-extensions](https://github.com/ppKrauss/language-tag-extensions) is 'DATA'  

### DEV vs DATA
> [food-inspections-evaluation](https://github.com/Chicago/food-inspections-evaluation) is 'DEV'.

### Websites
> Decision if Web or Dev depends on complexity of website.   
> **Note:** We changed the official class-description from only _personal_ 'static website' to **just** 'static website'. This constraint didn't seem plausible.
> [OpenDuka](https://github.com/OpenInstitute/OpenDuka) is 'DEV' as it contains a MVC-Model and acts as a Web-App rather than a static website.
> > This question has been officially answered: https://github.com/InformatiCup/InformatiCup2017/issues/8
### Collection of tips
> **Example:** 'Collection of Android tips' is educational so 'EDU' is the way to go.

### Collection of problems vs answers to them
> Whereas answers to possible questions are of an educational origin, the sole collection of such should be seen as a collection.    
> In the first case choose 'EDU', else 'DOCS'.  

### Dummy repositories
> If the focus of a repository lays on the existence of it only and not on storage of information (repository is _almost_ empty or does'nt contain any files), we call it a **Dummy** repository.  
> Even such repository is subject to practice or homework, 'OTHER' should be chosen nevertheless.  
> [This repo is for demonstration purposes only.](https://github.com/octocat/Spoon-Knife)

### Data-Visualization
> If repo contains dataset and visualization as well, 'DATA' should still be chosen.    
> Although this applies only to repositories that contain such datasets. If datasets in general can be used for these programs, 'DEV' is the better choice.  

### DOCS vs EDU
> A bug reproduction description that does not contain the solution (no educational value) -> DOCS
> **Example** [Bug description](https://api.github.com/repos/GrahamDennis/spark-kryo-serialisation)
> This question has been officially answered: https://github.com/InformatiCup/InformatiCup2017/issues/9

### DOCS vs DEV
> A repository containing a project structure always tends to be DEV. Only if the readme implies to be categorised as DOCS, it should be classified as such.
> A project primarily used for storing files, even if those files are code and get small changes, is still docs
> A **single commit** of a **fully developed** project tends to be rather DOCS than DEV.
> **Example** [Code stored for creating a tutorial](https://github.com/yahwin/backbone-tutorials)

### EDU vs HW
> Homework instructions and the work on some homework is HW. However, if only homework solutions are stored somewhere,
> along with other code for educational purposes it´s EDU? Did only encounter this a single time so far, can still be changed.
> **Example** [Code related to an educational book, which also contains exercises] https://github.com/alakras/javaForTestersCode

### Example / showcase projects
> EDU

### Websites for lectures
> [CS231n](https://github.com/cs231n/cs231n.github.io) is a 'WEB'-repository as focus clearly is on presentation of information and not improvement of them.

### 
> java-tdd-challenge is HW as it is an exercise. But the informaticup-repo on the other hand probably isn't HW.
