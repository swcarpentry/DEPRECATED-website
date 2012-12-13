#!/usr/bin/env python
'''Create a JSON blob for a badge, then fetch the badge itself.'''

import sys
import os
import datetime
import urllib2
import getopt

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

USAGE = '''Usage:
  create: badge.py -c base_dir username email [%(kinds)s]
  erase:  badge.py -e base_dir username [%(kinds)s]
  help:   badge.py -h''' % {'kinds' : '|'.join(BADGE_KINDS)}

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

BASE_URL = "http://beta.openbadges.org/baker?assertion=http://software-carpentry.org"

#-------------------------------------------------------------------------------

def make_paths(base_dir, username, kind, cannot_exist=True):
    '''Create, check, and return the paths used by handlers.'''

    # Sanity checks.
    assert kind in BADGE_DESCRIPTIONS, \
           'Unknown kind "%s"' % kind

    assert os.path.isdir(base_dir), \
           'Base directory "%s" not found' % base_dir

    json_dir = os.path.join(base_dir, 'badges', kind)
    assert os.path.isdir(json_dir), \
           'No such directory "%s"' % json_dir

    img_src_path = os.path.join(base_dir, 'img', 'badges', '%s.png' % kind)
    assert os.path.isfile(img_src_path), \
           'No such image file "%s"' % img_src_path

    # Construct and return paths and URL.
    json_name = '%s.json' % username
    json_path = os.path.join(json_dir, json_name)
    if cannot_exist:
        assert not os.path.isfile(json_path), \
               'JSON file "%s" already exists' % json_path

    img_dst_name = '%s-%s.png' % (username, kind)
    img_dst_path = os.path.join(base_dir, 'img', 'badges', img_dst_name)
    if cannot_exist:
        assert not os.path.isfile(img_dst_path), \
               'PNG file "%s" already exists' % img_dst_path

    json_url = os.path.join('/badges', kind, json_name)
    full_url = BASE_URL + json_url

    return json_path, img_dst_path, full_url

#-------------------------------------------------------------------------------

def create(base_dir, username, email, kind):
    '''Create a new badge.'''

    # Paths
    json_path, img_path, url = make_paths(base_dir, username, kind)

    # When is the badge being created?
    when = datetime.date.today().isoformat()

    # Create and save the JSON blob.
    values = {'username'    : username,
              'email'       : email,
              'kind'        : kind,
              'when'        : when,
              'name'        : BADGE_DESCRIPTIONS[kind][0],
              'description' : BADGE_DESCRIPTIONS[kind][1]}
    blob = JSON_TEMPLATE % values
    writer = open(json_path, 'w')
    writer.write(blob)
    writer.close()
    print 'JSON badge manifest saved to', json_path

    # Create and save the signed badge.
    reader = urllib2.urlopen(url)
    data = reader.read()
    reader.close()
    writer = open(img_path, 'wb')
    writer.write(data)
    writer.close()
    print 'PNG image saved to', img_path

#-------------------------------------------------------------------------------

def erase(base_dir, username, kind):
    '''Erase an existing badge.'''
    json_path, img_path, url = make_paths(base_dir, username, kind, False)
    if os.path.isfile(json_path):
        os.unlink(json_path)
    if os.path.isfile(img_path):
        os.unlink(img_path)

#-------------------------------------------------------------------------------

def usage():
    '''Print usage message and exit.'''
    print USAGE
    sys.exit(0)

#-------------------------------------------------------------------------------

if __name__ == '__main__':

    assert len(sys.argv) > 1, USAGE

    if sys.argv[1] == '-c':
        assert len(sys.argv) == 6, USAGE
        base_dir, username, email, kind = sys.argv[2:]
        create(base_dir, username, email, kind)

    elif sys.argv[1] == '-e':
        assert len(sys.argv) == 5, USAGE
        base_dir, username, kind = sys.argv[2:]
        erase(base_dir, username, kind)

    elif sys.argv[1] == '-h':
        usage()
        sys.exit(0)

    else:
        print >> sys.stderr, USAGE
        sys.exit(1)
