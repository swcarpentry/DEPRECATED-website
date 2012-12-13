This directory holds the Software Carpentry 4.0 web site re-engineered
to use Jinja2 templates, so that pages can be compiled and served
statically, rather than being served by WordPress.  To recompile
everything, run 'make', then look in /tmp/swc/*.

To do:
- Auto-numbering of blog entries (somehow).
- Need an index of blog entries by category and by author.
- Potentially add RSS icon for subscribing.
- Fix the formatting/appearance of all the setup/*.html pages.

- class="author" in book/bib.html: no style defined for this, but we need the semantic info.  ('class="person" is bold italic, used in team.html --- not appropriate for here.)
