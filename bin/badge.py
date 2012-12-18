#!/usr/bin/env python
'''Create a JSON blob for a badge, then fetch the badge itself.'''

import sys
import os
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
    "version" : "0.1",
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
}
'''

REQUEST_URL = "http://beta.openbadges.org/baker?assertion=http://software-carpentry.org/"

USAGE = '''Usage:
badge.py create  image_src_dir badge_root_dir [%(kinds)s] username email
badge.py dummy   image_src_dir badge_root_dir [%(kinds)s] username email
badge.py erase   badge_root_dir [%(kinds)s] username
badge.py extract filename...
badge.py help''' % {'kinds' : '|'.join(BADGE_KINDS)}

#-------------------------------------------------------------------------------

def main(args):
    '''Main program driver.'''

    assert len(args) > 1, USAGE

    if args[1] in ('create', '--create', '-c'):
        assert len(args) == 7, USAGE
        image_src_dir, badge_root_dir, kind, username, email = args[2:7]
        create(image_src_dir, badge_root_dir, kind, username, email)

    if args[1] in ('dummy', '--dummy', '-d'):
        assert len(args) == 7, USAGE
        image_src_dir, badge_root_dir, kind, username, email = args[2:7]
        dummy(image_src_dir, badge_root_dir, kind, username, email)

    elif args[1] in ('erase', '--erase', '-e'):
        assert len(args) == 5, USAGE
        badge_root_dir, kind, username = args[2:5]
        erase(badge_root_dir, kind, username)

    elif args[1] in ('extract', '--extract', '-x'):
        assert len(args) >= 2, USAGE
        filenames = args[2:]
        extract(filenames)

    elif args[1] in ('help', '--help', '-h'):
        usage()
        sys.exit(0)

    else:
        print >> sys.stderr, USAGE
        sys.exit(1)

#-------------------------------------------------------------------------------

def create(image_src_dir, badge_root_dir, kind, username, email):
    '''Create a new badge.'''

    assertion, url, json_dst_path = \
        _setup(image_src_dir, badge_root_dir, kind, username, email)

    # Save assertion.
    with open(json_dst_path, 'w') as writer:
        writer.write(assertion)
    print 'JSON badge manifest saved to', json_path

    # Create and save the baked badge image.
    with urllib2.urlopen(url) as reader:
        data = reader.read()
    with open(image_dst_path, 'wb') as writer:
        writer.write(data)
    print 'PNG image saved to', image_dst_path

#-------------------------------------------------------------------------------

def dummy(image_src_dir, badge_root_dir, kind, username, email):
    '''Construct and display everything that would be used to generate a badge.'''

    assertion, url, image_dst_path, json_dst_path = \
        _setup(image_src_dir, badge_root_dir, kind, username, email)

    print 'URL:', url
    print 'Baked badge:', image_dst_path
    print 'JSON file:', json_dst_path
    print 'Assertion:'
    print assertion

#-------------------------------------------------------------------------------

def erase(badge_root_dir, kind, username):
    '''Erase an existing badge's image and JSON files.'''

    _, image_dst_path, json_dst_path, _ = \
        _make_paths(image_src_dir, badge_root_dir, kind, username, False)

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

def _setup(image_src_dir, badge_root_dir, kind, username, email):
    '''Set up for badge generation (shared between creation and dummy run).'''

    # Paths
    image_src_path, image_dst_path, json_dst_path, url = \
        _make_paths(image_src_dir, badge_root_dir, kind, username)

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

    return assertion, url, image_dst_path, json_dst_path

#-------------------------------------------------------------------------------

def _make_paths(image_src_dir, badge_root_dir, kind, username, cannot_exist=True):
    '''Create, check, and return the paths used by handlers.'''

    # Badge type is recognized.
    assert kind in BADGE_DESCRIPTIONS, \
           'Unknown kind "%s"' % kind

    # Badge image source exists.
    assert os.path.isdir(image_src_dir), \
           'Image source directory "%s" not found' % image_src_dir
    image_src_path = os.path.join(image_src_dir, '%s.png' % kind)
    assert os.path.isfile(image_src_path), \
           'No such image file "%s"' % image_src_path

    # Badge storage directory exists.
    assert os.path.isdir(badge_root_dir), \
           'Badge root directory "%s" not found' % badge_root_dir
    badge_dst_dir = os.path.join(badge_root_dir, kind)
    assert os.path.isdir(badge_dst_dir), \
           'Badge destination directory "%s" not found' % badge_dst_dir

    # Baked badge image.
    image_dst_path = os.path.join(badge_dst_dir, '%s.png' % username)
    if cannot_exist:
        assert not os.path.isfile(image_dst_path), \
               'Baked badge image file "%s" already exists' % image_dst_path

    # Name of JSON file.
    json_name = '%s.json' % username

    # JSON file.
    json_dst_path = os.path.join(badge_dst_dir, json_name)
    if cannot_exist:
        assert not os.path.isfile(json_dst_path), \
               'JSON file "%s" already exists' % json_dst_path

    # URL for badge baking request.
    url = REQUEST_URL + os.path.join(badge_root_dir, kind, json_name)

    return image_src_path, json_dst_path, image_dst_path, url

#-------------------------------------------------------------------------------

if __name__ == '__main__':
    main(sys.argv)
