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

# website user@hostname
WEBSITE_USERHOST = swcarpentry@software-carpentry.org

# Standard site compilation arguments.
COMPILE = \
	python bin/compile.py \
	-d $$(date "+%Y-%m-%d") \
	-o $(OUT_DIR) \
	-p . -p bootcamps -p people -p credits -p 3_0 -p 4_0 -p blog \
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

#------------------------------------------------------------

.default : commands

## commands     : show all commands
commands :
	@grep -E '^##' Makefile | sed -e 's/## //g'

#------------------------------------------------------------

## install      : rebuild entire site for real.
install :
	@make OUT_DIR=$(HOME)/software-carpentry.org SITE=http://software-carpentry.org check

## install-bare : rebuild entire site for real, without checks.
install-bare :
	@make OUT_DIR=$(HOME)/software-carpentry.org SITE=http://software-carpentry.org check-bare

## install-rsync: rebuild entire site locally, and then rsync to the webhost
install-rsync :
	@make SITE=http://software-carpentry.org check
	rsync -avz "$(OUT_DIR)/" "$(WEBSITE_USERHOST):software-carpentry.org/"

## install-dev-rsync: rebuild entire site locally as (dev.s-c.org), and then rsync to the webhost
install-dev-rsync :
	@make SITE=http://dev.software-carpentry.org check
	rsync -avz "$(OUT_DIR)/" "$(WEBSITE_USERHOST):dev.software-carpentry.org/"

## check        : rebuild entire site locally for checking purposes.
check : $(STATIC_DST) $(OUT_DIR)/.htaccess
	@make ascii-chars
	@make check-bare
	@make check-links

## check-bare   : rebuild entire site locally, but do not validate html 
check-bare: $(STATIC_DST) $(OUT_DIR)/.htaccess
	$(COMPILE) -m metadata.json -r $(BLOG_RSS_FILE) -c $(ICALENDAR_FILE) index.html

## blog-next-id : find the next blog entry ID to use.
blog-next-id :
	@expr 1 + $$(fgrep -h post_id blog/*/*/*.html \
	| sed -e 's:<meta name="post_id" content="::g' -e 's:" />::g' \
	| sort -n \
	| tail -1)

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

## tidy         : clean up local files.
tidy :
	rm -f *~ */*~ */*/*~ */*/*/*~

## clean        : clean up generated files (but not copied files).
clean : tidy
	rm -f $$(find $(OUT_DIR) -name '*.html' -print)

## sterile      : clean up everything.
sterile : tidy
	rm -rf $(OUT_DIR)

