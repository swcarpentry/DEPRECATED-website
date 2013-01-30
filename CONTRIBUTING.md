Contributing to Software Carpentry
==================================

Software Carpentry is an open source/open access project, and we
welcome contributions of all kinds.  By contributing, you are agreeing
that Software Carpentry may redistribute your work under
[these licenses][licenses].  Please see [this page][creators] for
a list of contributors to date.

Workflow
--------

Software Carpentry uses a development workflow similar to that of
[AstroPy][] and many other open source projects. The AstroPy docs have
excellent sections on:

* [Getting started with git][astropy-git]
* [Developer workflow][astropy-workflow]

[AstroPy]: http://astropy.org
[astropy-git]: http://astropy.readthedocs.org/en/latest/development/workflow/index.html#getting-started-with-git
[astropy-workflow]: http://astropy.readthedocs.org/en/latest/development/workflow/development_workflow.html
[creators]: http://software-carpentry.org/badges/creator.html
[licenses]: http://software-carpentry.org/license.html

Blogging 
--------

To create a new blog post, here is what you do: 

1. Clone swcarpentry/website on GitHub.
2. Clone that to your desktop.
3. In the root directory, run 'make blog-next-id' to find out what ID number your blog post should have.  (This will eventually be automated.)
4. Create a file called blog/YYYY/MM/some-descriptive-title.html (where 'YYYY' is the four-digit year and 'MM' is the two-digit month, but you knew that).  Alternatively, copy blog/YYYY/MM/something-or-other.html to create the file you want.
5. Edit the metadata at the top of the file:
  - "post_id" is whatever step 3 returned
  - "author_id" must be one of the short strings from blog/metadata.json.  If the person supposedly authoring the post isn't in that file, add 'em.
  - "title" is the post title.  It can't contain special characters right now (will be fixed).
  - "post_date" is self-explanatory.
  - There can be any number of "category" meta's.  The values must be taken from the second half of blog/metadata.json (again, if you need a new category, add it).
6. Put HTML between the {% block content %} and {% endblock content %} markers.
  - If you need to refer to our email address, it is {{contact_email}} (double curlies).
  - If you need to refer to a file, use {{root_path}}/path/to/file.
  - We also provide {{site}} (the base URL for the site), {{twitter_name}}, and {{twitter_url}} (hopefully self-explanatory.
  - I'll add {{facebook_url}} if someone can remind me what it is.
  - If you're attaching a file, put the file in files/YYYY/MM/some-name-or-other, and refer to it as {{root_path}}/files/YYYY/MM/some-name-or-other
7. 'make check' in the root directory to create build/*.html (to make sure all the HTML validates, all the file paths resolve, etc.).
8. Open build/blog/index.html or build/blog/YYYY/MM/some-descriptive-title.html to eyeball your creation.
9. When you're satisfied, 'git add blog/YYYY/MM/some-descriptive-title.html' (*not* build/anything, ever).  Also 'git add' any extra files you've created (attachments).
10. 'git commit -m "Adding a blog post about something or other"' will commit it to your local copy (on your laptop).
11. 'git push origin master' will push it to your clone on GitHub (assuming you've configured 'origin' to mean "my clone on GitHub").
12. Go to GitHub and issue a pull request from your clone to swcarpentry/website, then assign it to me or Jon for proof-reading.
