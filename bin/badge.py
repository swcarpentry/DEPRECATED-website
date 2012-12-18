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
%(name)s create  image_src_dir badge_root_dir [%(kinds)s] username email
%(name)s dummy   image_src_dir badge_root_dir [%(kinds)s] username email
%(name)s erase   badge_root_dir [%(kinds)s] username
%(name)s extract filename...
%(name)s help''' % {'name' : sys.argv[0], 'kinds' : '|'.join(BADGE_KINDS)}

#-------------------------------------------------------------------------------

def main(args):
    '''Main program driver.'''

    if len(args) <= 1:
        usage()

    elif args[1] in ('create', '--create', '-c'):
        assert len(args) == 7, USAGE
        image_src_dir, badge_root_dir, kind, username, email = args[2:7]
        create(image_src_dir, badge_root_dir, kind, username, email)

    elif args[1] in ('dummy', '--dummy', '-d'):
        assert len(args) == 7, USAGE
        image_src_dir, badge_root_dir, kind, username, email = args[2:7]
        create(image_src_dir, badge_root_dir, kind, username, email, bake=False)

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

    else:
        usage()

#-------------------------------------------------------------------------------

def create(image_src_dir, badge_root_dir, kind, username, email, bake=True):
    '''Create a new badge.  If 'bake' is True, bake a real badge; if it's false,
    just copy the badge image file (for testing).'''

    # Paths
    image_src_path, image_dst_path, json_dst_path, url = \
        _make_paths(badge_root_dir, kind, username, image_src_dir=image_src_dir)

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

def erase(badge_root_dir, kind, username):
    '''Erase an existing badge's image and JSON files.'''

    _, image_dst_path, json_dst_path, _ = \
        _make_paths(badge_root_dir, kind, username, cannot_exist=False)

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

def _make_paths(badge_root_dir, kind, username, image_src_dir=None, cannot_exist=True):
    '''Create, check, and return the paths used by handlers.'''

    # Badge type is recognized.
    assert kind in BADGE_DESCRIPTIONS, \
           'Unknown kind "%s"' % kind

    # Badge image source exists.
    if image_src_dir is None:
        image_src_path = None
    else:
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

    return image_src_path, image_dst_path, json_dst_path, url

#-------------------------------------------------------------------------------

if __name__ == '__main__':
    main(sys.argv)
