# Installation Manual

## Requirements

* Python 2.7 64bit 
* pip (module manager)
* Firefox >= 50
* Screen size >= (1280px x 600px)
* RAM >= 4GB

## Notes

This guide can be followed to get the frontend running on your local system. If you don't want to install one of the listed dependencies or want to emulate a preconfigured client image, please refer to the section `VirtualBox`. Even though the recommended way is not to run the client in an emulation.

Please make sure that the working / installation **directory** of python and the g++ compiler do **not contain special characters** such as umlauts.
Keep in mind that installations with pip require **super user rights**.

## Modules

_Either installed with `pip install xxx` (on UNIX systems) or downloaded and installed with the command `pip install path/to/file.whl` (on Windows)._ 

1. [numpy + mkl](http://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy)
2. [scipy](http://www.lfd.uci.edu/~gohlke/pythonlibs/#scipy)
3. [paste](http://www.lfd.uci.edu/~gohlke/pythonlibs/#paste)

_Installed with the command `pip install xxx`_

1. bottle
2. keras
3. sklearn
4. nltk
5. gensim
6. pattern
7. theano

## Other

* [Microsoft Visual C++ Compiler for Python 2.7](https://www.microsoft.com/en-us/download/details.aspx?id=44266)
* [A 64bit g++ compiler](http://deeplearning.net/software/theano/install_windows.html#gcc)
* Keras has to be configured to use theano (instead of tensorflow). In UNIX systems, this can be changed at `~/.keras/keras.json`.

## When everything is said and done

Now that every library and dependency is installed, you can open the **command shell** in the folder `Application`. Type `python start.py` and wait until the GUI is being opened in a new Tab in Firefox (this may take a couple of minutes). You can learn how to interact with the GUI in a separate documentation file `Frontend Manual.md`. Note that can can read the docfiles in the User Interface as well.

_Note: If there are still packages missing that do not show up in the list, please install them via pip._


## VirtualBox

Instead of installing everything from above, you can also use the VM image. A virtualisation software such as Oracle VirtualBox is needed in this case as well as a unzipping tool such as 7Zip. Please be sure to reservate enough RAM for the emulation.

 > [Download link](https://drive.google.com/drive/folders/0B3nBoE608aQyaG9iZkk0UFFpSm8?usp=sharing) < 

Root login credentials are
```
Username: informaticup
Password: informaticup
```

GitHub credentials for [our project](https://github.com/Ichaelus/Github-Classifier) are
```
Username: InformatiCupClient
Password: InformatiCupClient1
```

Once Ubuntu has booted, change to the folder `~/GithubClassificator/Application` and replace it with the folder `Application` of our submission. Open the folder and run `sudo python start.py` inside the terminal.

## And what about the Backend?

We had many thoughts about running the backend locally as well or not. This would imply running two localhosts (Apache with PHP and Bottle with Python) synchronously as well as a local MySQL database - all that leads to many irrelevant and OS-restricted dependencies.

Therefore we decided to rely on the remote server even in the final submission, while providing you both the running source code (located in the folder `/Backend/`) and full access to the server and its database.

```
Accessible via PuTTY on SSH port 7822
IP:  67.209.116.156
Username: root
Password: d4b4176bd5443f89
Backend location: /var/www/html
Database access: http://67.209.116.156/phpmyadmin/
Database username: root
Database password: c99t6%3NSjte7eaub8iw7y1a!
```