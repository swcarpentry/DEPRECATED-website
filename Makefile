# Host site.
SITE = http://software-carpentry.org

# Output directory (will be created).
OUT_DIR = /tmp/swc

# Blog feed index.
BLOG_RSS_FILE = $(OUT_DIR)/feed.xml

# Standard site compilation arguments.
COMPILE = \
	python2.7 bin/compile.py \
	-d $$(date "+%Y-%m-%d") \
	-o $(OUT_DIR) \
	-p . -p bootcamps -p 3_0 -p 4_0 -p blog \
	-s $(SITE) \
	-v

# Static files.
STATIC_SRC = $(wildcard ./css/*.css) \
             $(wildcard ./css/bootstrap/*.css) \
             $(wildcard ./css/bootstrap/img/*.png) \
             $(wildcard ./files/*.bib) \
             $(wildcard ./files/papers/*.pdf) \
             $(wildcard ./files/*/*/*.*) \
             $(wildcard ./img/*.ico) \
             $(wildcard ./img/*.png) \
             $(wildcard ./img/*/*.gif) \
             $(wildcard ./img/*/*.jpg) \
             $(wildcard ./img/*/*.png) \
             $(wildcard ./js/*.js) \
             $(wildcard ./js/bootstrap/*.js) \
             $(wildcard ./3_0/*/*.jpg) \
             $(wildcard ./3_0/*/*.png) \
             $(wildcard ./4_0/*/*.odp) \
             $(wildcard ./4_0/*/*.pdf) \
             $(wildcard ./4_0/*/*/*.mp3) \
             $(wildcard ./4_0/*/*/*.png) \
             $(wildcard ./book/img/*/*.jpg) \
             $(wildcard ./book/img/*/*.png) \
             $(wildcard ./book/src/*/*.csv) \
             $(wildcard ./book/src/*/*.html) \
             $(wildcard ./book/src/*/*.py) \
             $(wildcard ./book/src/*/*.sql) \
             $(wildcard ./book/src/*/*.txt) \
             $(wildcard ./book/src/*/*.xml) 
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

## commands   : show all commands
commands :
	@grep -E '^##' Makefile | sed -e 's/## //g'

#------------------------------------------------------------

## all-dev    : build and install everything into dev.software-carpentry.org
all-dev :
	make OUT_DIR=$(HOME)/dev.software-carpentry.org SITE=http://dev.software-carpentry.org site

#------------------------------------------------------------

## site       : rebuild entire site.
site : $(STATIC_DST) $(OUT_DIR)/.htaccess
	$(COMPILE) -m blog/metadata.json -r $(BLOG_RSS_FILE) index.html
	@make journal
	@make links
	@make figref

## site-about : make the 'about' pages.
site-about :
	$(COMPILE) about/index.html

## site-blog  : make the blog alone
site-blog :
	$(COMPILE) -m blog/metadata.json blog/index.html

## site-book  : make the book alone
site-book :
	$(COMPILE) book/index.html
	@make figref

## site-boot  : make the bootcamps alone
site-boot :
	$(COMPILE) bootcamps/index.html

## site-3.0   : make the 3.0 notes alone
site-3.0 :
	$(COMPILE) 3_0/index.html

## site-4.0   : make the 4.0 notes alone
site-4.0 :
	$(COMPILE) 4_0/index.html

## figref     : patch cross-references in figures
figref :
	@python bin/fignumber.py $(BOOK_CHAPTERS_HTML)

## journal    : make journal-format version of blog
journal :
	python bin/journal.py ${OUT_DIR}/blog/*/*/*.html > ${OUT_DIR}/blog/journal.html

#------------------------------------------------------------

## valid      : check that generated HTML is valid.
valid :
	@python bin/validxml.py $(BLOG_RSS_FILE) $$(find $(OUT_DIR) -name '*.html' -print)

## links      : check that local links resolve in generated HTML.
links :
	@find $(OUT_DIR) -type f -print | python bin/links.py $(OUT_DIR)

## chars      : check for non-ASCII characters or tab characters.
chars :
	@python bin/chars.py $$(find . -name '*.html' -print)

# Copy static files.
$(STATIC_DST) : $(OUT_DIR)/% : %
	@mkdir -p $$(dirname $@)
	cp $< $@

$(OUT_DIR)/.htaccess : _htaccess
	cp $< $@

#------------------------------------------------------------

## bib        : check for undefined/unused bibliography references.
bib :
	@bin/book.py bibundef $(BOOK_CHAPTERS_HTML)
	@bin/book.py bibunused $(BOOK_CHAPTERS_HTML)

## check      : run all checks.
check :
	@for i in unknown gloss images source structure bib fig; do \
	  echo '----' $$i '----'; \
	  make $$i; \
	done

## classes    : list all classes used in the generated HTML files.
classes :
	@bin/book.py classes $$(find $(OUT_DIR) -name '*.html' -print)

## fig        : check figure formatting and for undefined/unused figures.
fig :
	@bin/book.py figformat $(BOOK_CHAPTERS_HTML)
	@bin/book.py figundef $(BOOK_CHAPTERS_HTML)
	@bin/book.py figunused $(BOOK_CHAPTERS_HTML)

## fix        : count FIXME markers in files.
fix :
	@bin/book.py fix $(BOOK_CHAPTERS_HTML)

## gloss      : check glossary formatting and for undefined/unused glossary entries.
gloss :
	@bin/book.py glossformat $(BOOK_CHAPTERS_HTML)
	@bin/book.py glossundef $(BOOK_CHAPTERS_HTML)
	@bin/book.py glossunused $(BOOK_CHAPTERS_HTML)

## ideas      : extract key ideas.
ideas :
	@bin/book.py ideas $(BOOK_CHAPTERS_HTML)

## images     : check for undefined/unused images.
images :
	@bin/book.py imgundef img $(BOOK_CHAPTERS_HTML)
	@bin/book.py imgunused img $(BOOK_CHAPTERS_HTML)

## source     : check for undefined/unused source code fragments.
source :
	@bin/book.py srcundef src $(BOOK_CHAPTERS_HTML)
	@bin/book.py srcunused src $(BOOK_CHAPTERS_HTML)

## structure  : check overall structure of files.
structure :
	@bin/book.py structure $(BOOK_CHAPTERS_HTML)

## summaries  : extract section summaries (learning goals and keypoints).
summaries :
	@bin/book.py summaries $(BOOK_CHAPTERS_HTML)

## unknown    : check for unexpected HTML files.
unknown :
	@bin/book.py unknown vol1 $(BOOK_CHAPTERS_HTML)

## words-a    : count words in files (report alphabetically).
words-a :
	@bin/book.py words $(BOOK_CHAPTERS_HTML)

## words-n    : count words in files (report numerically).
words-n :
	@bin/book.py words $(BOOK_CHAPTERS_HTML) | sort -n -r -k 2

#------------------------------------------------------------

## tidy       : clean up local files.
tidy :
	rm -f *~ */*~ */*/*~ */*/*/*~

## clean      : clean up generated files (but not copied files).
clean : tidy
	rm -f $$(find $(OUT_DIR) -name '*.html' -print)

## sterile    : clean up everything.
sterile : tidy
	rm -rf $(OUT_DIR)
