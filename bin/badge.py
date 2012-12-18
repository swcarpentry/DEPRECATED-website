#!/usr/bin/env python
'''Create a JSON blob for a badge, then bake the badge itself.'''

import sys
import os
import getopt
import datetime
import urllib2
import getopt
import png

#-------------------------------------------------------------------------------

BADGE_DESCRIPTIONS = {
    'core'       : ['Core Skills',
                    'Unix shell, version control, programming, and testing'],
    'instructor' : ['Instructor',
                    'Teaching at workshops or online'],
    'organizer'  : ['Organizer',
                    'Organizing workshops and learning groups'],
    'creator'    : ['Creator',
                    'Creating learning materials and other content']
}

BADGE_KINDS = BADGE_DESCRIPTIONS.keys()
BADGE_KINDS.sort()

JSON_TEMPLATE = '''{
  "recipient" : "%(email)s",
  "issued_on" : "%(when)s",
  "badge" : {
    "version" : "5.0",
    "name" : "%(name)s",
    "image" : "/img/badges/%(kind)s.png",
    "description" : "%(description)s",
    "criteria" : "/badges/%(kind)s.html",
    "issuer" : {
      "origin" : "http://software-carpentry.org",
      "name" : "Software Carpentry",
      "contact" : "admin@software-carpentry.org"
    }
  }
}'''

REQUEST_URL = "http://beta.openbadges.org/baker?assertion=http://software-carpentry.org/"

USAGE = '''Usage:
%(name)s -a create -i image_src_dir -w website_dir -b badge_root_dir -k [%(kinds)s] -u username -e email
%(name)s -a dummy  -i image_src_dir -w website_dir -b badge_root_dir -k [%(kinds)s] -u username -e email
%(name)s -a erase                   -w website_dir -b badge_root_dir -k [%(kinds)s] -u username
%(name)s -a extract filename...
%(name)s -a help''' % {'name' : sys.argv[0], 'kinds' : '|'.join(BADGE_KINDS)}

#-------------------------------------------------------------------------------

def main(args):
    '''Main program driver.'''

    action = None
    image_src_dir = None
    website_dir = None
    badge_dir = None
    kind = None
    username = None
    email = None

    options, filenames = getopt.getopt(args[1:], 'a:b:e:i:k:u:w:')
    for opt, arg in options:

        # Action.
        if opt == '-a':
            assert action is None, \
                   'Action specified multiple times (-a)'
            assert arg in ('create', 'dummy', 'erase', 'extract', 'help'), \
                   'Unknown action "%s"' % arg
            action = arg

        # Badges directory within web site directory.
        elif opt == '-b':
            assert badge_dir is None, \
                   'Badges directory specified multiple times (-b)'
            badge_dir = arg

        # Email.
        elif opt == '-e':
            assert email is None, \
                   'Email specified multiple times (-e)'
            email = arg

        # Image source directory.
        elif opt == '-i':
            assert image_src_dir is None, \
                   'Image source directory specified multiple times (-i)'
            image_src_dir = arg

        # Kind of badge.
        elif opt == '-k':
            assert kind is None, \
                   'Kind of badge specified multiple times (-k)'
            kind = arg

        # Username.
        elif opt == '-u':
            assert username is None, \
                   'Username specified multiple times (-u)'
            username = arg

        # Web site directory.
        elif opt == '-w':
            assert website_dir is None, \
                   'Web site directory specified multiple times (-w)'
            website_dir = arg

    # Despatch.
    if action is None:
        usage()

    elif action == 'create':
        create(image_src_dir, website_dir, badge_dir, kind, username, email)

    elif action == 'dummy':
        create(image_src_dir, website_dir, badge_dir, kind, username, email,
               bake=False)

    elif action == 'erase':
        erase(website_dir, badge_dir, kind, username)

    elif action == 'extract':
        assert len(filenames) > 0, \
               'No filenames given for metadata extraction'
        extract(filenames)

    elif action == 'help':
        usage()

#-------------------------------------------------------------------------------

def create(image_src_dir, website_dir, badge_dir, kind, username, email, bake=True):
    '''Create a new badge.  If 'bake' is True, bake a real badge; if it's false,
    just copy the badge image file (for testing).'''

    # Paths
    image_src_path, image_dst_path, json_dst_path, url = \
        _make_paths(website_dir, badge_dir, kind, username, image_src_dir=image_src_dir)
    print 'Badge baking URL:', url

    # When is the badge being created?
    when = datetime.date.today().isoformat()

    # Create and save the JSON assertion.
    values = {'username'    : username,
              'email'       : email,
              'kind'        : kind,
              'when'        : when,
              'name'        : BADGE_DESCRIPTIONS[kind][0],
              'description' : BADGE_DESCRIPTIONS[kind][1]}
    assertion = JSON_TEMPLATE % values
    print 'Badge assertion...'
    print assertion

    # Save assertion.
    with open(json_dst_path, 'w') as writer:
        writer.write(assertion)
    print 'JSON badge manifest path:', json_dst_path

    # Create and save the baked badge image?
    if bake:
        print 'Badge baking URL:', url
        with urllib2.urlopen(url) as reader:
            data = reader.read()
    else:
        with open(image_src_path, 'rb') as reader:
            data = reader.read()
    with open(image_dst_path, 'wb') as writer:
        writer.write(data)
    print 'Badge image path:', image_dst_path

#-------------------------------------------------------------------------------

def erase(website_dir, badge_dir, kind, username):
    '''Erase an existing badge's image and JSON files.'''

    _, image_dst_path, json_dst_path, _ = \
        _make_paths(website_dir, badge_dir, kind, username, cannot_exist=False)

    if os.path.isfile(json_dst_path):
        os.unlink(json_dst_path)

    if os.path.isfile(image_dst_path):
        os.unlink(image_dst_path)

#-------------------------------------------------------------------------------

def extract(filenames):
    '''Extract metadata URL from files.'''
    for f in filenames:
        try:
            p = png.Reader(filename=f)
            for chunk_type, chunk_data in p.chunks():
                if chunk_type == 'tEXt':
                    who, what = chunk_data.split('\x00')
                    if who == 'openbadges':
                        print '%s: %s' % (filename, what)
                        break
            else:
                print >> sys.stderr, 'No open badges metadtata found in', f
        except Exception, e:
            print >> sys.stderr, "error in %s:" % f, e

#-------------------------------------------------------------------------------

def usage():
    '''Print usage message and exit.'''
    print USAGE
    sys.exit(0)

#-------------------------------------------------------------------------------

def _make_paths(website_dir, badge_dir, kind, username,
                image_src_dir=None, cannot_exist=True):
    '''Create, check, and return the paths used by handlers.'''

    # Badge type is recognized.
    assert kind in BADGE_DESCRIPTIONS, \
           'Unknown kind of badge "%s"' % kind

    # Web site directory.
    assert website_dir is not None, \
           'Web site directory "%s" not provided' % website_dir
    assert os.path.isdir(website_dir), \
           'Web site directory "%s" does not exist' % website_dir

    # Full Badge directory.
    assert badge_dir is not None, \
           'Badge sub-directory not provided' % badge_dir
    badge_root_dir = os.path.join(website_dir, badge_dir)
    assert os.path.isdir(badge_root_dir), \
           'Badge root directory "%s" does not exist' % badge_root_dir
    badge_kind_dir = os.path.join(badge_root_dir, kind)
    assert os.path.isdir(badge_kind_dir), \
           'Badge kind directory "%s" does not exist' % badge_kind_dir

    # Badge image source.
    if image_src_dir is None:
        image_src_path = None
    else:
        assert os.path.isdir(image_src_dir), \
               'Image source directory "%s" not found' % image_src_dir
        image_src_path = os.path.join(image_src_dir, '%s.png' % kind)
        assert os.path.isfile(image_src_path), \
               'No such image file "%s"' % image_src_path

    # Baked badge image.
    image_dst_path = os.path.join(badge_kind_dir, '%s.png' % username)
    if cannot_exist:
        assert not os.path.isfile(image_dst_path), \
               'Baked badge image file "%s" already exists' % image_dst_path

    # Name of JSON file.
    json_name = '%s.json' % username

    # JSON file.
    json_dst_path = os.path.join(badge_kind_dir, json_name)
    if cannot_exist:
        assert not os.path.isfile(json_dst_path), \
               'JSON file "%s" already exists' % json_dst_path

    # URL for badge baking request.
    url = REQUEST_URL + os.path.join(badge_dir, kind, json_name)

    return image_src_path, image_dst_path, json_dst_path, url

#-------------------------------------------------------------------------------

if __name__ == '__main__':
    main(sys.argv)
