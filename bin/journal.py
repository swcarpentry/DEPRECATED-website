#!/usr/bin/env python

import sys
import re

HEADER = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html>
  <head>
    <link rel="shortcut icon" type="image/x-icon" href="../img/favicon.ico" />
    <link href="../css/bootstrap/bootstrap.css" rel="stylesheet" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link href="../css/bootstrap/bootstrap-responsive.css" rel="stylesheet" />
    <link rel="stylesheet" type="text/css" href="../css/swc.css" />
    <link rel="stylesheet" type="text/css" href="../css/swc-bootstrap.css" />
    <link rel="alternate" type="application/rss+xml" title="The Software Carpentry Blog RSS Feed" href="/tmp/swc/feed.xml"/>
    <!-- override article title centering -->
    <style type="text/css">
      div.title {
        text-align: left;
        padding: 10px 40px;
      }
    </style>
    <!-- HTML5 shim, for IE6-8 support of HTML5 elements -->
    <!--[if lt IE 9]>
      <script src="http://html5shim.googlecode.com/svn/trunk/html5.js"></script>
    <![endif]-->
    <title>Software Carpentry Blog</title>
  </head>
  <body>
    <div class="container">
      <div class="banner">
        <a href="../index.html" title="Software Carpentry Home">
          <img src="../img/software-carpentry-banner.png" alt="Software Carpentry banner" />
        </a>
      </div>
"""

ENTRY = """
      <div class="title">
        <h2>%(title)s</h2>
      </div>
      <div class="row-fluid">
        <div class="span10 offset1">
%(body)s
        </div>
      </div>
"""

FOOTER = """
    </div>
  </body>
</html>
"""

Post_Id_Pat = re.compile('<meta\s+name="post_id"\s+content="([^"]+)"\s*/>')
Journal_Pat = re.compile('<meta\s+name="journal"\s+content="([^"]+)"\s*/>')
Title_Pat = re.compile('<h1>(.+)</h1>')
Body_Pat = re.compile('<div class="span10 offset1">(.+)<div id="disqus_thread">', re.DOTALL)

#----------------------------------------

def extract(filename):
    with open(filename, 'r') as reader:
        data = reader.read()
    m = Journal_Pat.search(data)
    if (not m) or (m.group(1).lower() != 'true'):
        return None
    post_id = int(Post_Id_Pat.search(data).group(1))
    title = Title_Pat.search(data).group(1)
    body = Body_Pat.search(data).group(1).strip().replace('../../..', '..')
    return (post_id, ENTRY % {'title' : title, 'body' : body})

#----------------------------------------

if __name__ == '__main__':
    assert len(sys.argv) > 1, 'Need at least one post filename'
    print(HEADER)
    entries = [extract(filename) for filename in sys.argv[1:]]
    entries = [e for e in entries if e]
    entries.sort()
    for e in entries:
        print(e[1])
    print(FOOTER)
