#!/usr/bin/env python

"""
What we have right now looks like this:

* All of our pages and blog posts are .html files, rather than
  Markdown or reST.  This is primarily because we inherited most of
  those pages from an earlier website, and it was easier to leave them
  in that format than convert.

* We use Jinja2 as a templating engine.  A small number of pages are
  one-of-a-kind (e.g., the ./index.html home page for the site).

* Three kinds of pages are highly repeated, and each currently
  requires special handling in our Python compilation script.

  * bootcamps/yyyy-mm-site.html (e.g., bootcamps/2012-07-paris.html):
    there are about 25 of these right now, and we expect to add
    several per month going forward (one for each two-day workshop we
    run).  A lot of the content (e.g., setup instructions for
    students) is generic, and is contained in other .html files that
    are included by reference.  However, in order to construct the
    bootcamps/index.html page, we need to read in all the
    bootcamp-specific pages, sort by date, and divide them into two
    groups (those coming up and those past).  We figure out what files
    to load using a file glob, since we can get the start date needed
    for sorting from the metadata embedded in the bootcamp files.

  * 4_0/lecture/topic.html (e.g., 4_0/python/func.html): there are
    about 140 of these pages.  Each is a short tutorial on a
    particular subject (e.g., Python functions), and they are grouped
    into directories (e.g., one for Python, one for regular
    expressions, and so on).  The special processing here is that
    4_0/index.html needs a list of all the lecture titles, and the
    lectures all need lists of the topics they contain.  Right now, we
    do this via explicit includes: there's a bunch of <meta...> tags
    at the top of 4_0/index.html referring to the
    4_0/lecture/index.html pages, and each of those pages uses
    <meta...> tags to refer to tutorial files, e.g.:

    <meta name="subfile" content="func.html" />

    What makes things more complicated is that each lecture's
    index.html page (e.g., 4_0/python/index.html) has a couple of
    paragraphs at the top to introduce key points, enclosed in:

    {% block introduction %}
      ...stuff...
    {% endblock introduction %}

    We extract these blocks from those files and insert them into
    4_0/index.html when compiling to produce the little 'ads' you see
    in http://dev.software-carpentry.org/4_0/index.html under each
    section title.

  * blog/yyyy/mm/name-name-name.html (e.g.,
    blog/2012/11/web-4-science.html).  These are blog posts, with a
    bit of metadata at the top (in <meta...> tags) with the author,
    the date, and a serial number:

    {% extends "_blog.html" %}
    {% block file_metadata %}
    <meta name="post_id" content="5239" />
    <meta name="author_id" content="pipitone.j" />
    <meta name="title" content="Pelican Guts: on content management for Software Carpentry" />
    <meta name="post_date" content="2012-11-01" />
    <meta name="category" content="tooling" />
    {% endblock file_metadata %}
    {% block content %}
    <p>...actual blog post content...</p>
    {% endblock content %}

    Again, we find posts using a file glob, extract the post_id
    fields, sort, and use that information to order them, fill in the
    index, etc.  (We have to use a serial post ID rather than the date
    because we often have several posts on the same date.  That's also
    what we inherited when we extracted all of this from WordPress.)
"""

import sys
import os
import glob
import re
import getopt
import json
import jinja2
import time
import datetime
try:  # Python 3
    from urllib.parse import urlparse, urljoin
except ImportError:  # Python 2
    from urlparse import urlparse, urljoin

from PyRSS2Gen import RSS2, RSSItem, Guid

#----------------------------------------

CONTACT_EMAIL = 'info@software-carpentry.org'
TWITTER_NAME = '@swcarpentry'
TWITTER_URL = 'https://twitter.com/swcarpentry'

METADATA_TEMPLATE = r'<meta\s+name="%s"\s+content="([^"]*)"\s*/>'

MONTHS = {
    '01' : 'Jan', '02' : 'Feb', '03' : 'Mar', '04' : 'Apr',
    '05' : 'May', '06' : 'Jun', '07' : 'Jul', '08' : 'Aug',
    '09' : 'Sep', '10' : 'Oct', '11' : 'Nov', '12' : 'Dec'
}

BLOG_DESCRIPTION = 'Helping scientists make better software since 1998'
BLOG_HISTORY_LENGTH = 10
BLOG_TITLE = 'Software Carpentry'
BLOG_EXCERPT_LENGTH = 200
BLOG_CONTENT_PATTERN = re.compile(r'{% block content %}(.+){% endblock content %}', re.DOTALL)
BLOG_TAG_REPLACEMENT_PATTERN = re.compile(r'<[^>]+>')

#----------------------------------------

def timestamp():
    """Return the current UTC time formatted in ISO 8601
    """
    return time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())


class Application(object):
    """
    Manage the application:
    * Parse command-line arguments.
    * Manage a dictionary of standard Jinja2 variables used in all pages.
    * Create the Jinja2 template expansion environment.
    * Manage blog metadata (mapping aliases to author names, topic names, etc.).
    """

    def __init__(self, args):
        """
        Initialize settings, parse command line, create rendering environment.
        """
        self.env = None
        self.metadata = None
        self.output_dir = None
        self.blog_filename = None
        self.icalendar_filename = None
        self.search_path = []
        self.site = None
        self.today = None
        self.verbosity = 0

        self.filenames = self._parse(args)
        self._build_env()
        self._load_metadata()

    def standard(self, filename):
        """
        Return dictionary of standard page elements for a file.
        (Filename needed so we can calculate root path.)
        """
        depth = len([x for x in os.path.dirname(filename).split('/') if x])
        if depth == 0:
            root_path = '.'
        else:
            root_path = '/'.join([os.pardir] * depth)
        return {'contact_email' : CONTACT_EMAIL,
                'filename'      : filename,
                'root_path'     : root_path,
                'site'          : self.site,
                'timestamp'     : timestamp(),
                'today'         : self.today,
                'twitter_name'  : TWITTER_NAME,
                'twitter_url'   : TWITTER_URL}

    def _parse(self, args):
        """
        Parse command-line options.
        """
        options, filenames = getopt.getopt(args, 'c:d:m:o:p:r:s:v')
        for opt, arg in options:
            if opt == '-c':
                assert self.icalendar_filename is None, \
                       'iCalendar filename specified multiple times'
                self.icalendar_filename = arg
            elif opt == '-d':
                self.today = arg
            elif opt == '-m':
                assert self.metadata is None, \
                       'Blog metadata specified multiple times'
                self.metadata = arg
            elif opt == '-o':
                assert self.output_dir is None, \
                       'Destination directory specified multiple times'
                self.output_dir = arg
            elif opt == '-p':
                assert os.path.isdir(arg), \
                       'Search path directory "%s" not found' % arg
                self.search_path.append(arg)
            elif opt == '-r':
                assert self.blog_filename is None, \
                       'RSS filename specified multiple times'
                self.blog_filename = arg
            elif opt == '-s':
                self.site = arg
            elif opt == '-v':
                self.verbosity += 1
            else:
                assert False, \
                'Unknown option %s' % opt

        assert self.today is not None, \
               'No date set (use -d)'
        assert self.output_dir is not None, \
               'No destination directory specified (use -o)'
        assert self.search_path, \
               'No search path directories specified (use -p)'
        assert self.site is not None, \
               'No site specified (use -s)'

        return filenames

    def _build_env(self):
        """
        Create template expansion environment.
        """
        loader = jinja2.FileSystemLoader(self.search_path)
        self.env = jinja2.Environment(loader=loader,
                                      autoescape=True)

    def _load_metadata(self):
        """
        Load blog metadata translation information (if specified).
        """
        if self.metadata is None:
            self.metadata = {}
        else:
            with open(self.metadata, 'r') as reader:
                self.metadata = json.load(reader)

#----------------------------------------

class GenericPage(object):
    """
    Store information gleaned from a Jinja2 template page.
    * KEYS defines the names of <meta...> tag elements looked for.
      Subclasses must inherit this variable or define one of their own
      with the same name.
    * UPLINK is how to get 'up' in the hierarchy (e.g., up to the
      index page for a lesson).
    """

    KEYS = '*subfile *subglob title'.split()
    UPLINK = ''

    def __init__(self, app, factory, filename, original, parent):
        """
        Initialize page representation from file.  This is the
        template method pattern: derived classes may override any or
        all of file loading, metadata extraction, finalizing this
        object, loading subfiles, and finalizing the child objects
        representing those children.
        """
        self.app = app
        self.filename = filename
        self.original = original
        self.parent = parent
        self.children = []
        self.uplink = self.UPLINK

        self._factory = factory
        self._directory = os.path.dirname(filename)
        self._sort_key = None

        self._load_file()
        self._get_metadata()
        self._finalize_self()
        self._load_subfiles()
        self._finalize_children()

    def link(self):
        """
        Return the URL for linking to this page from a sibling.
        May be overriden in derived classes.
        """
        return os.path.basename(self.filename)

    def render(self):
        """
        Render this page and its children.
        """
        self._render()
        for child in self.children:
            child.render()

    def _load_file(self):
        """
        Load file data, which is then stored as a single block of
        characters and as a list of lines (since we need both in
        different cases).
        """
        with open(self.filename, 'r') as reader:
            self._data = reader.read()
        self._block = self._data
        self._lines = self._block.split('\n')

    def _get_patterns(self):
        """
        Return triples of (field name, default value, regexp) for
        matching metadata fields.  Requires this class to have a
        'KEYS' member.  If a key name starts with a '*', the key can
        have multiple values.
        """
        result = []
        for k in self.KEYS:
            multi, default = k.startswith('*'), None
            if multi:
                k, default = k[1:], []
            r = re.compile(METADATA_TEMPLATE % k)
            result.append([k, default, r])
        return result

    def _get_metadata(self):
        """
        Extract metadata embedded in <meta...> tags using the patterns
        constructed by _get_patterns.  These values are stored as
        member variables in this object.
        """
        for (field, default, pat) in self._get_patterns():
            self._set_metadata(field, default)
            for line in self._lines:
                match = pat.search(line)
                if match:
                    self._set_metadata(field, match.group(1))

    def _set_metadata(self, field, value):
        """
        Store metadata extracted from a <meta...> tag as a member
        variable of this object.
        """
        # Member variable doesn't exist at all yet, so assign value.
        # If the key can have multiple values, the initial value must
        # be a list.
        if field not in self.__dict__:
            assert value in (None, []), \
                   'Must initialize to None (single) or [] (multi)'
            self.__dict__[field] = value

        # Member variable already exists and is a list, so the
        # variable can be multi-valued, so append.
        elif type(self.__dict__[field]) is list:
            self.__dict__[field].append(value)

        # Member variable already exists, so check that its value is
        # None (i.e., that it hasn't already been initialized), and
        # then set its value.
        else:
            assert self.__dict__[field] is None, \
                   'Single-valued field %s being reset' % field
            self.__dict__[field] = value

    def _load_subfiles(self):
        """
        Load sub-files recursively.
        """

        # Get children that are named explicitly.
        self.children = [self._factory(os.path.join(self._directory, sf), sf, self)
                         for sf in self.subfile]

        # Get children by globbing.
        sort = False
        if 'subglob' in self.__dict__:
            sort = True
            for sg in self.subglob:
                whole_glob = os.path.join(self._directory, sg)
                matches = [self._factory(m, None, self)
                           for m in glob.glob(whole_glob)]
                self.children += matches

        # If anything was globbed, sort everything (including children
        # that were loaded explicitly).
        if sort:
            self.children.sort(key=lambda x: (x._sort_key, id(x)))

    def _finalize_children(self):
        """
        Create prev/next links between children.
        """
        for (i, child) in enumerate(self.children):
            child.prev = None if (i == 0) \
                         else self.children[i-1].link()
            child.next = None if (i == len(self.children)-1) \
                         else self.children[i+1].link()

    def _render(self):
        """
        Render and save this page.
        """
        if self.app.verbosity > 0:
            sys.stderr.write(self.filename)
            sys.stderr.write('\n')

        # Render.
        template = self.app.env.get_template(self.filename)
        result = template.render(page=self,
                                 **self.app.standard(self.filename))

        # Make sure the output directory exists.
        dest = os.path.join(self.app.output_dir, self.filename)
        directory = os.path.dirname(dest)
        if not os.path.isdir(directory):
            os.makedirs(directory)

        # Save the rendered text.
        with open(dest, 'w') as writer:
            writer.write(result)

    def _finalize_self(self):
        """
        Template method: finalize elements in this object.
        """
        pass

#----------------------------------------

class BootCampPage(GenericPage):
    """
    Represent information about a boot camp.
    The 'Instances' class variable keeps track of all created instances,
    so that they can be used to render the iCalendar feed.
    """

    KEYS = GenericPage.KEYS + \
           ['venue', 'latlng', 'date', 'startdate', 'enddate',
            'eventbrite_key']

    UPLINK = 'index.html'

    Instances = []

    def __init__(self, *args):
        GenericPage.__init__(self, *args)
        BootCampPage.Instances.append(self)

    def _finalize_self(self):
        """
        Finish creating this object:
        * Create normalized date for display.
        * Create slug.
        * Create sort key (start date and venue).
        """
        self._merge_dates()
        self.slug = os.path.splitext(os.path.basename(self.filename))[0]
        self._sort_key = (self.startdate, self.venue)

    def _merge_dates(self):
        """
        Merge start and end dates into human-readable form.
        """
        start, end = self.startdate, self.enddate

        start_year, start_month, start_day = start.split('-')
        start_month_name = MONTHS[start_month]

        # One-day workshop.
        if end is None:
            self.date = '%s %s, %s' % \
                        (start_month_name, start_day, start_year)
            return

        end_year, end_month, end_day = end.split('-')
        end_month_name = MONTHS[end_month]

        # Spans two years.
        if start_year < end_year:
            self.date = '%s %s, %s - %s %s, %s' % \
                        (start_month_name, start_day, start_year,
                         end_month_name, end_day, end_year)

        # Spans two months.
        elif start_month < end_month:
            self.date = '%s %s - %s %s, %s' % \
                        (start_month_name, start_day,
                         end_month_name, end_day, end_year)

        # All in one month.
        elif start_day < end_day:
            self.date = '%s %s-%s, %s' % \
                        (start_month_name, start_day,
                         end_day, end_year)

        # End date is before start date?
        else:
            assert False, \
                   'Bad date range %s -- %s' % (start, end)

    def index_link(self):
        """
        Link from index page to this post.
        FIXME: must be a better way than special-casing this.
        """
        return 'bootcamps/{0}'.format(self.link())

#----------------------------------------

class LessonPage(GenericPage):
    """
    Represent information about a lesson made up of topics.
    """

    UPLINK = '../index.html'

    KEYPOINTS = re.compile(r'<ul\s+class="keypoints"\s*>(.+?)</ul>', re.DOTALL)

    def link(self):
        """
        Return the URL for linking to this page from a sibling by
        hacking around with the file path.
        """
        lowest_dir = self._directory.split('/')[-1]
        return os.path.join(os.pardir, lowest_dir, 'index.html')

    def _finalize_self(self):
        """
        Finish creating this lessage page:
        * The slug for a lesson is the last directory in path (since the
          main lesson file is always 'index.html').
        * Extract the keypoints from this lesson for inclusion in the main
          index page.
        """
        self.slug = os.path.dirname(self.filename).split('/')[-1]
        m = self.KEYPOINTS.search(self._data)
        assert m, \
               'No keypoints found in %s' % self.filename
        self.keypoints = m.group(1)

#----------------------------------------

class TopicPage(GenericPage):
    """
    Represent information about a single topic within a lesson.
    """

    UPLINK = 'index.html'

    def _finalize_self(self):
        """
        Finish creating this topic's page object:
        * The slug for a topic is the base of the filename.
        """
        self.slug = os.path.splitext(os.path.basename(self.filename))[0]

#----------------------------------------

class BlogIndexPage(GenericPage):
    """
    Singleton to store information about all blog posts.
    """

    def __init__(self, *args):
        GenericPage.__init__(self, *args)
        self.blog_history_length = BLOG_HISTORY_LENGTH

    def _finalize_children(self):
        """
        Extract information about years and months for creating the
        table of blog posts as well as linking children.
        """

        # Link children as usual.
        GenericPage._finalize_children(self)

        # Extract information needed for index table.
        self.years = sorted(set(c.year for c in self.children))
        self.months = sorted(MONTHS.keys())
        self._posts = {}
        for child in self.children:
            year, month = child.year, child.month
            if (year, month) not in self._posts:
                self._posts[(year, month)] = []
            self._posts[(year, month)].append(child)

    def posts(self, year, month):
        """
        Get all blog posts for a specific period.
        """
        return self._posts.get((year, month), [])

    def month_name(self, month):
        """
        Convert 2-digit month number into month name (helper function
        for template expansion).
        """
        return MONTHS[month]

#----------------------------------------

class BlogPostPage(GenericPage):
    """
    Represent information about a single blog post.
    The 'Instances' class variable keeps track of all created instances,
    so that they can be used to render the blog feed.
    """

    KEYS = GenericPage.KEYS + \
           ['post_id', 'post_date', 'author_id', '*category']

    UPLINK = '../../index.html'

    Instances = []

    def __init__(self, *args):
        GenericPage.__init__(self, *args)
        BlogPostPage.Instances.append(self)

    def link(self):
        """
        Return the URL for linking to this page from a sibling.  This
        is completely tied to the year/month/post directory structure
        right now.
        """
        return '/'.join(['..', '..', self.year, self.month, self.name])

    def index_link(self):
        """
        Link from index page to this post.
        FIXME: must be a better way than special-casing this.
        """
        return '/'.join([self.year, self.month, self.name])

    def excerpt(self):
        """
        Return an excerpt of the page for display in the RSS reader by:
        * finding the content block
        * replacing HTML tags
        * taking the first few hundred characters
        * going back from the end of that to the first space
        * hoping the result isn't too horribly mangled.
        The right way to do this would be to have an explicit excerpt
        div or span in the blog posts, but that's not what we inherited
        from WordPress.
        """
        result = 'No description available'
        if self.content:
            result = BLOG_TAG_REPLACEMENT_PATTERN.sub('', self.content)
            result = result[:BLOG_EXCERPT_LENGTH]
            if ' ' in result:
                result = result[:result.rindex(' ')]
            if result:
                result += ' [...]'
        return result

    def _finalize_self(self):
        """
        Record this page's creation so that the index can be constructed.
        Translate metadata.
        """

        def _tx(key, value):
            return self.app.metadata[key][value]

        self._sort_key = int(self.post_id)
        self.year, self.month, self.name = self.filename.split('/')[-3:]

        self.content = None
        m = BLOG_CONTENT_PATTERN.search(self._block)
        if m:
            self.content = m.group(1)

        for key in self.app.metadata:
            if key not in self.__dict__:
                pass
            elif type(self.__dict__[key]) is str:
                self.__dict__[key] = _tx(key, self.__dict__[key])
            elif type(self.__dict__[key]) is list:
                self.__dict__[key] = [_tx(key, v) for v in self.__dict__[key]]
            else:
                assert False, 'Bad metadata translation setup'

#----------------------------------------

class PageFactory(object):
    """
    Construct the right kind of page object for a page by finding a
    pageclass comment in the page or its parent(s) and looking up the
    corresponding class in this script.  Page class mappings are
    cached to avoid repeatedly reading the same handful of generic
    (base) Jinja2 templates.
    """

    PAGE_CLASS_PAT = re.compile(r'<!--\s+pageclass:\s+\b(.+)\b\s+-->')
    EXTENDS_PAT = re.compile(r'{%\s*extends\s+"([^"]+)"\s*%}')

    def __init__(self, app):
        self.app = app
        self.cache = {}

    def __call__(self, filename, original, parent):
        """
        Make a page object based on metadata embedded in the page itself.
        """
        with open(filename, 'r') as reader:
            cls = self._find_page_class(filename)
            assert cls in globals(), \
                   'Unknown page class %s' % cls
            return globals()[cls](self.app, self, filename, original, parent)

    def _find_page_class(self, original_filename):
        """
        Search recursively for page class, returning the page's class.
        """

        # Page class has already been determined and cached.
        filename = self._find_file(original_filename)
        if filename in self.cache:
            return self.cache[filename]

        with open(filename, 'r') as reader:

            # Explicit page class declaration in this page.
            data = reader.read()
            m = self.PAGE_CLASS_PAT.search(data)
            if m:
                cls = m.group(1)
                self.cache[filename] = cls
                return cls

            # This page extends something else.
            m = self.EXTENDS_PAT.search(data)
            if m:
                base_filename = m.group(1)
                cls = self._find_page_class(base_filename)
                self.cache[filename] = cls
                return cls

            # No page class.
            assert False, \
                   'Unable to find page class for %s' % filename

    def _find_file(self, filename):
        """
        Search for a file in various directories by name.  This
        duplicates the machinery inside Jinja2 for finding template
        pages that are being extended, but there's no easy way to get
        Jinja2 to do the finding for us.
        """
        for d in self.app.search_path:
            f = os.path.join(d, filename)
            if os.path.isfile(f):
                return f
        assert False, \
               'File %s not found in search path %s' % (filename, self.app.search_path)

#----------------------------------------

class ContentEncodedRSSItem(RSSItem): 
    def __init__(self, **kwargs): 
        self.content = kwargs.get('content', None)
        if 'content' in kwargs: 
            del kwargs['content']
        RSSItem.__init__(self, **kwargs)

    def publish_extensions(self, handler): 
        if self.content:
            handler._out.write('<%(e)s><![CDATA[%(c)s]]></%(e)s>' %
                { 'e':'content:encoded', 'c':self.content})
                
#----------------------------------------

class ContentEncodedRSS2(RSS2): 
    def __init__(self, **kwargs):
        RSS2.__init__(self, **kwargs)
        self.rss_attrs['xmlns:content']='http://purl.org/rss/1.0/modules/content/' 


#----------------------------------------

def create_rss(filename, site, posts):
    """
    Generate RSS2 feed.xml file for blog.
    """
    
    items = []
    slice = posts[-BLOG_HISTORY_LENGTH:]
    slice.reverse()

    for post in slice:
        template_vars = post.app.standard(post.filename)
        template_vars['root_path'] = site
        path = os.path.join(site, 'blog', post.index_link())
        rendered_content = jinja2.Template(post.content).render(**template_vars)
        items.append(ContentEncodedRSSItem(title=post.title,
                             author=post.author_id,
                             link=path,
                             description=post.excerpt(),
                             content=rendered_content,
                             pubDate=post.post_date))

    rss = ContentEncodedRSS2(title=BLOG_TITLE,
               link=site,
               description=BLOG_DESCRIPTION,
               lastBuildDate=datetime.datetime.utcnow(),
               items=items)

    with open(filename, 'w') as writer:
        rss.write_xml(writer)

#----------------------------------------

class ICalendarWriter(object):
    """
    iCalendar generator for boot camps.
    The format is defined in RFC 5545: http://tools.ietf.org/html/rfc5545
    """

    def __call__(self, filename, site, bootcamps):
        lines = [
            'BEGIN:VCALENDAR',
            'VERSION:2.0',
            'PRODID:-//Software Carpentry/Boot Camps//NONSGML v1.0//EN',
        ]
        for bootcamp in bootcamps:
            lines.extend(self.bootcamp(site, bootcamp))
        lines.extend(['END:VCALENDAR', ''])
        content = '\r\n'.join(lines)
        # From RFC 5545, section 3.1.4 (Character Set):
        # The default charset for an iCalendar stream is UTF-8.
        with open(filename, 'wb') as writer:
            writer.write(content.encode('utf-8'))

    def bootcamp(self, site, bootcamp):
        uid = '{0}@{1}'.format(bootcamp.link().replace('.html', ''),
                               urlparse(site).netloc or 'software-carpentry.org')
        url = urljoin(site, bootcamp.index_link())
        if bootcamp.enddate:
            end_fields = [int(x) for x in bootcamp.enddate.split('-')]
        else:  # one day boot camp?
            end_fields = [int(x) for x in bootcamp.startdate.split('-')]
        end = datetime.date(*end_fields)
        dtend = end + datetime.timedelta(1)  # non-inclusive end date
        lines = [
            'BEGIN:VEVENT',
            'UID:{0}'.format(uid),
            'DTSTAMP:{0}'.format(timestamp()),
            'DTSTART;VALUE=DATE:{0}'.format(bootcamp.startdate.replace('-', '')),
            'DTEND;VALUE=DATE:{0}'.format(dtend.strftime('%Y%m%d')),
            'SUMMARY:{0}'.format(self.escape(
                    '{0}, {1}'.format(bootcamp.venue, bootcamp.date))),
            'DESCRIPTION;ALTREP="{0}":{0}'.format(url),
            'LOCATION:{0}'.format(self.escape(bootcamp.venue)),
        ]
        if bootcamp.latlng:
            lines.append('GEO:{0}'.format(bootcamp.latlng.replace(',', ';')))
        lines.append('END:VEVENT')
        return lines

    def escape(self, value):
        """
        Escape text following RFC 5545.
        """
        for char in ['\\', ';', ',']:
            value = value.replace(char, '\\' + char)
        value.replace('\n', '\\n')
        return value

#----------------------------------------

def main(args):
    """
    Main driver:
    * construct an application manager
    * construct a page factory
    * create and render page objects for each page (recursively)
    * generate the blog's feed.xml file if asked to do so
    """
    app = Application(args)
    factory = PageFactory(app)
    for filename in app.filenames:
        page = factory(filename, filename, None)
        page.render()
    if app.blog_filename:
        create_rss(app.blog_filename, app.site, BlogPostPage.Instances)
    if app.icalendar_filename:
        icw = ICalendarWriter()
        icw(app.icalendar_filename, app.site, BootCampPage.Instances)

#----------------------------------------

if __name__ == '__main__':
    main(sys.argv[1:])
