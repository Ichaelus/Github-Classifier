Your application should come with an install and user manual.


## Notes

The working / installation directory of python and the g++ compiler must not contain special character such as umlauts.
Please keep in mind that installations with pip require cmd to be started with admin rights.

## Modules

_Installed with the command `pip install path/to/file.whl`_

1. numpy + mkl (from http://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy)
2. scipy (from http://www.lfd.uci.edu/~gohlke/pythonlibs/#scipy)
3. paste (from http://www.lfd.uci.edu/~gohlke/pythonlibs/#paste)

_Installed with the command `pip install xxx`_

1. bottle
2. keras
3. sklearn
4. nltk
5. selenium
6. gensim
7. pattern
8. theano

## Other

* (Microsoft Visual C++ Compiler for Python 2.7)[https://www.microsoft.com/en-us/download/details.aspx?id=44266]
* (64bit g++ compiler)[http://deeplearning.net/software/theano/install_windows.html#gcc]
* Keras has to be configured to use theano (instead of tensorflow). In Unix systems, this can be changed at ~/.keras/keras.json.

## VirtualBox

Instead of installing everything from above, you can also use the VM image. A virtualisation software such as Oracle VirtualBox is needed in this case.

Login credentials are
Username: informaticup
Password: informaticup

Git credentials are
Username: InformatiCupClient
Password: InformatiCupClient1