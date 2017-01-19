# The database

This folder contains SQL dumps of the MySQL database running at the backend server. You can read further about the services provided by the PHP server at `Documentation/API.md`.

The database consists of a few similar structured tables containing partitions of our sample base:

* `unlabeled` contains samples without label that are being generated from randomly chosen GitHub repositories. Open the URL of the backend to mine additional samples in exchange for limited API calls
* `train` contains samples used to train classification modules
* `test` contains samples used to evaluate classfier outcome
* `standard_samples` contains samples given by InformatiCup guidelines
* `to_classify` contains samples chosen by Active Learning to be classified by a human