#!/usr/bin/env python

import sys
import os
import re
import glob
import json
from util import ET, read_xml, write_xml

#===============================================================================

FMT_BAD = '!'
FMT_UNDEF = '-'
FMT_UNUSED = '?'

PARENT_PREFIX = os.path.join(os.pardir, os.sep)

IDENTS = {'bib'   : [".//dl[@class='bib']/dt[@id]",
                     {'bookcite', 'papercite', 'webcite'}],
          'fig'   : [".//figure",
                     {'figref'}],
          'gloss' : [".//dl[@class='gloss']/dt[@id]",
                     {'gdef', 'gref'}]
         }

#===============================================================================

def _get_defs(doc, ident_key, format=set):
    def_xpath = IDENTS[ident_key][0]
    defs = doc.findall(def_xpath)
    ids = format(d.attrib['id'] for d in defs)
    return ids

#-------------------------------------------------------------------------------

def _get_refs(doc, ident_key, format=set):
    ref_classes = IDENTS[ident_key][1]
    result = format()
    for rc in ref_classes:
        xpath = ".//a[@class='%s']" % rc
        refs = doc.findall(xpath)
        try:
            ids = format(r.attrib['href'].split('#')[1] for r in refs)
        except IndexError, e:
            assert False, "Unable to parse %s" % [r.attrib['href'] for r in refs]
        if format is set:
            result.update(ids)
        elif format is list:
            result.extend(ids)
        else:
            assert False, "Unknown format %s" % format
    return result

#-------------------------------------------------------------------------------

def _get_defs_refs(filenames, ident_key):
    """
    Get definitions and cross-references from files.
    """

    defs = set()
    refs = set()
    for f in filenames:
        doc = read_xml(f)
        defs.update(_get_defs(doc, ident_key))
        refs.update(_get_refs(doc, ident_key))

    return defs, refs

#-------------------------------------------------------------------------------

def _get_fig_info(filename, fig):
    """
    Get figure ID and caption.
    """
    assert fig.attrib.get('id'), \
           "Figure(s) in %s missing id" % filename
    fig_id = fig.attrib.get('id')
    assert fig_id.startswith('f:'), \
           "Figure(s) in %s missing f: in id" % filename
    caption_node = _find_one_node(filename, fig, ".//figcaption")
    caption_fields = caption_node.text.split(':', 1)
    assert len(caption_fields) == 2, \
           "Badly formatted caption in %s for %s" % (filename, fig_id)
    assert caption_fields[0].startswith("Figure"), \
           "Caption in %s for Figure %s does not start with 'Figure'" % \
           (filename, fig_id)
    caption_text = caption_fields[1].lstrip()
    return fig_id, caption_text

#-------------------------------------------------------------------------------

def _get_points(filename, node, the_class):
    xpath = "./div[@class='%s']" % the_class
    points = node.findall(xpath)
    if not points:
        return None
    points = points[0].findall(".//ul")
    assert len(points) == 1, \
           'No list of type %s in section' % the_class
    points = points[0]
    points.tail = ''
    return ET.tostring(points)

#-------------------------------------------------------------------------------

def _find_files(child):
    """
    Find all files matching a pattern.
    """

    def callback(arg, directory, entries):
        if '.svn' in directory:
            return
        for e in entries:
            path = os.path.join(directory, e)
            if os.path.isfile(path):
                arg.add(path)

    result = set()
    os.path.walk(child, callback, result)
    return result

#-------------------------------------------------------------------------------

def _find_one_node(filename, root, xpath):
    """
    Find exactly one matching node or fail.
    """
    all_nodes = root.findall(xpath)
    assert len(all_nodes) == 1, \
        "Found %d matches for '%s' in %s" % \
        (len(all_nodes), xpath, filename)
    return all_nodes[0]

#-------------------------------------------------------------------------------

def _find_refs(filenames, element, attribute, strip=PARENT_PREFIX):
    """
    Find all references to files of a particular type.
    """
    xpath = ".//%s[@%s]" % (element, attribute)
    result = set()
    for f in filenames:
        doc = read_xml(f)
        nodes = doc.findall(xpath)
        vals = {n.attrib[attribute] for n in nodes}
        result.update(vals)
    result = {x.lstrip(strip) for x in result}
    return result

#-------------------------------------------------------------------------------

def _make_format(filenames):
    """
    Construct format for full width of all filenames.
    """
    return '%%-%ds' % max(len(f) for f in filenames)

#-------------------------------------------------------------------------------

def _remove_dir(filename):
    """
    Remove the directory portion from the filename.
    """
    return os.path.split(filename)[1]

#-------------------------------------------------------------------------------

def _show_set(prefix, values):
    """
    Display the values in a set as an ordered list.
    """
    values = list(values)
    values.sort()
    for v in values:
        print prefix, v

#===============================================================================

def bibundef(*filenames):
    """
    Look for undefined bibliography entries.
    """
    defs, refs = _get_defs_refs(filenames, 'bib')
    _show_set(FMT_UNDEF, refs - defs)

#-------------------------------------------------------------------------------

def bibunused(*filenames):
    """
    Look for unused bibliography entries.
    """
    defs, refs = _get_defs_refs(filenames, 'bib')
    _show_set(FMT_UNUSED, defs - refs)

#-------------------------------------------------------------------------------

def classes(*filenames):
    """
    List all the HTML classes used in a set of files.
    """
    result = set()
    for f in filenames:
        for n in read_xml(f).findall(".//*[@class]"):
            for a in n.attrib['class'].split():
                result.add(a)
    for r in sorted(result):
        print r

#-------------------------------------------------------------------------------

def echo(*filenames):
    """
    Parse and then print.
    """
    for f in filenames:
        doc = read_xml(f)
        print ET.tostring(doc.getroot())

#-------------------------------------------------------------------------------

def figformat(*filenames):
    """
    Check that figures are properly formatted.
    """
    for f in filenames:
        doc = read_xml(f)
        figures = doc.findall(".//figure")
        for fig in figures:
            fig_id, caption_text = _get_fig_info(f, fig)
            all_images = fig.findall(".//img")
            assert len(all_images) <= 1, \
                   "Two or more images in %s for %s" % (f, fig_id)
            if len(all_images) == 1: # some figures contain tables or code
                img = all_images[0]
                img_alt = img.attrib.get('alt')
                assert img_alt == caption_text, \
                       "Inconsistent alt and caption for Figure %s in %s: '%s' vs '%s'" % \
                       (fig_id, f, img_alt, caption_text)
                img_path = img.attrib.get('src')
                try:
                    img_basename = os.path.basename(os.path.splitext(img_path)[0])
                    assert fig_id.endswith(img_basename), \
                        "Figure id %s in %s inconsistent with image path %s" % \
                        (fig_id, f, img_path)
                except AttributeError, e:
                    assert False, \
                           "Failed to check path and id consistency of Figure %s in %s" % \
                           (fig_id, f)

#-------------------------------------------------------------------------------

def figundef(*filenames):
    """
    Look for undefined figures.
    """
    defs, refs = _get_defs_refs(filenames, 'fig')
    _show_set(FMT_UNDEF, refs - defs)

#-------------------------------------------------------------------------------

def figunused(*filenames):
    """
    Look for unused figures.
    """
    defs, refs = _get_defs_refs(filenames, 'fig')
    _show_set(FMT_UNUSED, defs - refs)

#-------------------------------------------------------------------------------

def fix(*filenames):
    """
    Count 'fixme' markers in files.
    """
    flags = 'fixme'.split()
    counts = {f:0 for f in flags}
    format = _make_format(filenames)
    print format % 'File',
    for flag in flags:
        print '%6s' % flag.lstrip('fix'),
    print
    for f in filenames:
        doc = read_xml(f)
        print format % f,
        for flag in flags:
            num = len(doc.findall(".//*[@class='%s']" % flag))
            counts[flag] += num
            print '%6d' % num,
        print
    print format % 'Total',
    for flag in flags:
        print '%6d' % counts[flag],
    print

#-------------------------------------------------------------------------------

def glossformat(*filenames):
    """
    Look for improperly formatted glossary references.
    """
    for f in filenames:
        doc = read_xml(f)
        refs = doc.findall(".//a[@href]")
        refs = [r for r in refs if r.attrib.get('href', '').startswith('glossary.html')]
        refs = [r for r in refs if r.attrib.get('class', '') != 'dfn']
        for r in refs:
            print '%s %s: %s' % (FMT_BAD, f, r.attrib['href'])

#-------------------------------------------------------------------------------

def glossundef(*filenames):
    """
    Look for undefined bibliography entries.
    """
    defs, refs = _get_defs_refs(filenames, 'gloss')
    _show_set(FMT_UNDEF, refs - defs)

#-------------------------------------------------------------------------------

def glossunused(*filenames):
    """
    Look for unused glossary entries.
    """
    defs, refs = _get_defs_refs(filenames, 'gloss')
    _show_set(FMT_UNUSED, defs - refs)

#-------------------------------------------------------------------------------

def imgundef(image_dir, *filenames):
    """
    Look for missing images.
    """
    files = _find_files(image_dir)
    refs = _find_refs(filenames, 'img', 'src')
    _show_set(FMT_UNDEF, refs - files)

#-------------------------------------------------------------------------------

def imgunused(image_dir, *filenames):
    """
    Look for unused images.
    """
    files = _find_files(image_dir)
    refs = _find_refs(filenames, 'img', 'src')
    _show_set(FMT_UNUSED, files - refs)

#-------------------------------------------------------------------------------

def ideas(*filenames):
    """
    Extract ideas from files and display in groups.
    """
    all_ideas = {}
    for f in filenames:
        doc = read_xml(f)
        for section in doc.findall(".//div[@class='keypoints']"):
            for example in section.findall(".//li[@idea]"):
                ideas = example.attrib['idea'].split(';')
                del example.attrib['idea']
                example.tag = 'a'
                example.attrib['href'] = '%s#%s' % (f, section.attrib.get('id'))
                example.tail = ''
                for i in ideas:
                    if i not in all_ideas:
                        all_ideas[i] = []
                    all_ideas[i].append(ET.tostring(example))
    for idea in all_ideas:
        print '<h2>%s</h2>' % idea
        print '<ul>'
        for item in all_ideas[idea]:
            print '  <li>%s</li>' % item
        print '</ul>'

#-------------------------------------------------------------------------------

def summaries(*filenames):
    """
    Extract goals and keypoints from files.
    """

    def _lecture(filename, doc):
        title = doc.findall(".//div[@class='title']")[0]
        title.text = title.text.strip()
        title.tag = 'h2'
        title.tail = ''
        print '<a href="%s">%s</a>' % (filename, ET.tostring(title))

    def _get_section_title(node):
        title = node.findall(".//h2")
        if not title:
            return None
        title = title[0]
        title.tag = 'h3'
        title.tail = ''
        return title

    def _sections(filename, doc):
        for s in doc.findall(".//section"):
            title = _get_section_title(s)
            if title is None:
                continue
            title = ET.tostring(title)
            understand = _get_points(filename, s, 'understand')
            keypoints = _get_points(filename, s, 'keypoints')
            if (not understand) and (not keypoints):
                continue
            assert understand and keypoints, \
                   'Section %s in %s has understanding/keypoints mis-match' % (title, filename)
            print '  <a href="%s#%s">%s</a>' % \
                  (filename, s.attrib.get('id'), title)
            print '<p><strong>Understand:</strong></p>%s\n<p><strong>Summary:</strong></p>%s' % \
                  (understand, keypoints)

    print '<html>'
    print '<body>'
    for f in filenames:
        doc = read_xml(f)
        _lecture(f, doc)
        _sections(f, doc)
    print '</body>'
    print '</html>'

#-------------------------------------------------------------------------------

def srcundef(source_dir, *filenames):
    """
    Look for missing source files.
    """
    files = _find_files(source_dir)
    refs = _find_refs(filenames, 'pre', 'src')
    _show_set(FMT_UNDEF, refs - files)

#-------------------------------------------------------------------------------

def srcunused(source_dir, *filenames):
    """
    Look for unused source files.
    """
    files = _find_files(source_dir)
    refs = _find_refs(filenames, 'pre', 'src')
    _show_set(FMT_UNUSED, files - refs)

#-------------------------------------------------------------------------------

def structure(*filenames):
    """
    Check overall structure of files.
    """
    for f in filenames:
        doc = read_xml(f)
        _find_one_node(f, doc, ".//div[@class='mainmenu']")
        _find_one_node(f, doc, ".//div[@class='footer']")
        doctype = _find_one_node(f, doc, ".//meta[@name='type']")
        if doctype.attrib["content"] != "chapter":
            continue
        _find_one_node(f, doc, ".//ol[@class='toc']")

#-------------------------------------------------------------------------------

def unknown(*filenames):
    """
    What book files exist that shouldn't?
    """
    actual = set(glob.glob("*.html"))
    expected = set(filenames)
    extras = list((actual - expected) - {"index.html"})
    if not extras:
        return
    extras.sort()
    for f in extras:
        print f

#-------------------------------------------------------------------------------

def valid(*filenames):
    """
    Check that all files are HTML compliant.
    """
    for f in filenames:
        doc = read_xml(f)
        if doc is None:
            print 'failed to parse "%s"' % f

#-------------------------------------------------------------------------------

def words(*filenames):
    """
    Count words in files (excluding code blocks).
    """
    format = _make_format(filenames)
    single = '%6d'
    total = 0
    for f in filenames:
        doc = read_xml(f)
        nodes = doc.findall(".//*")
        count = 0
        for n in nodes:
            if n.tag == 'pre':
                continue
            for x in (n.text, n.tail):
                if x:
                    count += len(x.split())
        print format % _remove_dir(f), single % count
        total += count
    print format % 'Total', single % total

#===============================================================================

if __name__ == '__main__':
    assert len(sys.argv) > 1, 'No command given'
    cmd, args = sys.argv[1], sys.argv[2:]
    assert cmd in locals(), 'Unknown command "%s"' % cmd
    locals()[cmd](*args)
