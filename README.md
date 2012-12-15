Software Carpentry Website
==========================

This is the uncompiled source for the Software Carpentry website at
http://software-carpentry.org.  If you have questions or suggestions,
please [contact us by email](mailto:info@software-carpentry.org).

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

Issue Labels
------------

We are using [GitHub issues](https://github.com/swcarpentry/website/issues?state=open)
to manage this project.  If you are creating or updating issues, please
label them as follows:

* `admin`: administrative tasks.
* `question`: self-explanatory; where possible, please add other labels to show what the question is about.
* `assessment`: anything related to measuring how we're doing.
* `bootcamp`: catch-all for things related to boot camps; use the more specific issues below if possible.
* `bootcamp-arrange`: arranging a boot camp (i.e., making initial contact, picking dates, etc.).
* `bootcamp-run`: running a boot camp once dates and instructors have been settled.
* `content creation`: creating something new on the web site, or new instructional material.
* `content enhancement`: upgrading existing material.
* `duplicate`: please always indicate which issue this one duplicates.
* `effort large`: this task will take weeks.
* `effort medium`: this task will take days.
* `effort small`: this task will take hours.
* `teaching practice`: related to *how* we teach.
* `tooling`: the task involves writing or upgrading software.
* `website`: the task is specifically related to our web site.
* `bug`: [something is wrong on the Internet](http://xkcd.com/386/).
* `invalid`: works as designed, etc.
