Software Carpentry Website
==========================

This is the uncompiled source for the Software Carpentry website
at http://software-carpentry.org.

Cloning
-------

We keep the 3.0 and 4.0 lesson materials in separate repositories which we include
here via [submodules](http://git-scm.com/book/en/Git-Tools-Submodules).
After cloning run the following commands to download the lesson materials:

    git submodule init
    git submodule update

Building
--------

Compiling the website requires [Python](http://python.org) and
[Jinja2](http://jinja.pocoo.org/).

* Type `make` to see a list of all available commands.
* Type `make check` to build everything in ./build for testing purposes.
* Type `make install` to build into $HOME/software-carpentry.org when logged into software-carpentry.org to update the live web site.
