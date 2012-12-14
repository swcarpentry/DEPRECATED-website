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

Use the `make site` command to compile. The compiled site is put it in `/tmp/swc`.
Type just `make` to see a list of all available commands.
