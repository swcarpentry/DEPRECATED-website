# This Makefile relies on two variables:
# OUT_DIR: where the web site is stored.
# SITE: the URL of the web site.
# By default, it builds into ./build.  The special target 'install'
# overrides the two variables and calls make recursively to build
# into to the installation directory on software-carpentry.org.

# Default value for output directory.
OUT_DIR = $(PWD)/build

# Default value for web site URL.
SITE = $(OUT_DIR)

# Blog feed index.
BLOG_RSS_FILE = $(OUT_DIR)/feed.xml

# iCalendar feed
ICALENDAR_FILE = $(OUT_DIR)/bootcamps.ics

# Standard site compilation arguments.
COMPILE = \
	python bin/compile.py \
	-d $$(date "+%Y-%m-%d") \
	-o $(OUT_DIR) \
	-p . -p bootcamps -p 3_0 -p 4_0 -p blog \
	-s $(SITE) \
	-v

# Static files.
STATIC_SRC = $(wildcard ./3_0/*/*.jpg) \
             $(wildcard ./3_0/*/*.png) \
             $(wildcard ./4_0/*/*.odp) \
             $(wildcard ./4_0/*/*.pdf) \
             $(wildcard ./4_0/*/*/*.mp3) \
             $(wildcard ./4_0/*/*/*.png) \
             $(wildcard ./badges/*/*.json) \
             $(wildcard ./badges/*/*.png) \
             $(wildcard ./book/img/*/*.jpg) \
             $(wildcard ./book/img/*/*.png) \
             $(wildcard ./book/src/*/*.csv) \
             $(wildcard ./book/src/*/*.html) \
             $(wildcard ./book/src/*/*.py) \
             $(wildcard ./book/src/*/*.sql) \
             $(wildcard ./book/src/*/*.txt) \
             $(wildcard ./book/src/*/*.xml) \
             $(wildcard ./css/*.css) \
             $(wildcard ./css/bootstrap/*.css) \
             $(wildcard ./css/bootstrap/img/*.png) \
             $(wildcard ./files/*.bib) \
             $(wildcard ./files/*/*/*.*) \
             $(wildcard ./files/papers/*.pdf) \
             $(wildcard ./img/*.ico) \
             $(wildcard ./img/*.png) \
             $(wildcard ./img/*/*.gif) \
             $(wildcard ./img/*/*.jpg) \
             $(wildcard ./img/*/*.png) \
             $(wildcard ./js/*.js) \
             $(wildcard ./js/bootstrap/*.js)
STATIC_DST = $(subst ./,$(OUT_DIR)/,$(STATIC_SRC))

# Chapters in book version.
BOOK_SUBJECTS_STEMS = \
  shell \
  svn \
  python \
  funclib \
  db \
  numpy \
  quality \
  setdict \
  dev \
  web \
  teach

BOOK_SUBJECTS_HTML = $(foreach stem,$(BOOK_SUBJECTS_STEMS),$(OUT_DIR)/book/$(stem).html)

# All chapters in book.
BOOK_CHAPTERS_STEMS = \
  index \
  intro \
  $(BOOK_SUBJECTS_STEMS) \
  concl \
  ack \
  bib \
  ref

BOOK_CHAPTERS_HTML = $(foreach stem,$(BOOK_CHAPTERS_STEMS),$(OUT_DIR)/book/$(stem).html)

#------------------------------------------------------------

.default : commands

## commands     : show all commands
commands :
	@grep -E '^##' Makefile | sed -e 's/## //g'

#------------------------------------------------------------

## install      : rebuild entire site for real.
install :
	@make OUT_DIR=$(HOME)/software-carpentry.org SITE=http://software-carpentry.org check

## check        : rebuild entire site locally for checking purposes.
check : $(STATIC_DST) $(OUT_DIR)/.htaccess
	@make ascii-chars
	$(COMPILE) -m blog/metadata.json -r $(BLOG_RSS_FILE) -c $(ICALENDAR_FILE) index.html
	@make blog-journal
	@make check-links
	@make book-figref

## blog-next-id : find the next blog entry ID to use.
blog-next-id :
	@expr 1 + $$(fgrep -h post_id blog/*/*/*.html \
	| sed -e 's:<meta name="post_id" content="::g' -e 's:" />::g' \
	| sort -n \
	| tail -1)

## blog-journal : make journal-format version of blog
blog-journal :
	python bin/journal.py ${OUT_DIR}/blog/*/*/*.html > ${OUT_DIR}/blog/journal.html

## check-links  : check that local links resolve in generated HTML.
check-links :
	@find $(OUT_DIR) -type f -print | python bin/links.py $(OUT_DIR)

## ascii-chars  : check for non-ASCII characters or tab characters.
ascii-chars :
	@python bin/chars.py $$(find . -name '*.html' -print)

#------------------------------------------------------------

# Copy static files.
$(STATIC_DST) : $(OUT_DIR)/% : %
	@mkdir -p $$(dirname $@)
	cp $< $@

$(OUT_DIR)/.htaccess : _htaccess
	cp $< $@

#------------------------------------------------------------

## book-bib     : check for undefined/unused bibliography references.
book-bib :
	@bin/book.py bibundef $(BOOK_CHAPTERS_HTML)
	@bin/book.py bibunused $(BOOK_CHAPTERS_HTML)

## book-book    : run all checks.
book-book :
	@for i in unknown gloss images source structure bib fig; do \
	  echo '----' $$i '----'; \
	  make book-$$i; \
	done

## book-classes : list all classes used in the generated HTML files.
book-classes :
	@bin/book.py classes $$(find $(OUT_DIR) -name '*.html' -print)

## book-fig     : check figure formatting and for undefined/unused figures.
book-fig :
	@bin/book.py figformat $(BOOK_CHAPTERS_HTML)
	@bin/book.py figundef $(BOOK_CHAPTERS_HTML)
	@bin/book.py figunused $(BOOK_CHAPTERS_HTML)

## book-figref  : patch cross-references in figures
book-figref :
	@python bin/fignumber.py $(BOOK_CHAPTERS_HTML)

## book-fix     : count FIXME markers in files.
book-fix :
	@bin/book.py fix $(BOOK_CHAPTERS_HTML)

## book-gloss   : check glossary formatting and for undefined/unused glossary entries.
book-gloss :
	@bin/book.py glossformat $(BOOK_CHAPTERS_HTML)
	@bin/book.py glossundef $(BOOK_CHAPTERS_HTML)
	@bin/book.py glossunused $(BOOK_CHAPTERS_HTML)

## book-ideas   : extract key ideas.
book-ideas :
	@bin/book.py ideas $(BOOK_CHAPTERS_HTML)

## book-images  : check for undefined/unused images.
book-images :
	@bin/book.py imgundef img $(BOOK_CHAPTERS_HTML)
	@bin/book.py imgunused img $(BOOK_CHAPTERS_HTML)

## book-source  : check for undefined/unused source code fragments.
book-source :
	@bin/book.py srcundef src $(BOOK_CHAPTERS_HTML)
	@bin/book.py srcunused src $(BOOK_CHAPTERS_HTML)

## book-struct  : check overall structure of files.
book-struct :
	@bin/book.py structure $(BOOK_CHAPTERS_HTML)

## book-summary : extract section summaries (learning goals and keypoints).
book-summary :
	@bin/book.py summaries $(BOOK_CHAPTERS_HTML)

## book-unknown : check for unexpected HTML files.
book-unknown :
	@bin/book.py unknown vol1 $(BOOK_CHAPTERS_HTML)

## book-words-a : count words in files (report alphabetically).
book-words-a :
	@bin/book.py words $(BOOK_CHAPTERS_HTML)

## book-words-n : count words in files (report numerically).
book-words-n :
	@bin/book.py words $(BOOK_CHAPTERS_HTML) | sort -n -r -k 2

#------------------------------------------------------------

## tidy         : clean up local files.
tidy :
	rm -f *~ */*~ */*/*~ */*/*/*~

## clean        : clean up generated files (but not copied files).
clean : tidy
	rm -f $$(find $(OUT_DIR) -name '*.html' -print)

## sterile      : clean up everything.
sterile : tidy
	rm -rf $(OUT_DIR)

