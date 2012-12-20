#!/usr/bin/env python2
#
# Copyright (C) 2012 W. Trevor King <wking@tremily.us>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the Creative Commons Attribution Unported
# License as published by the Creative Commons Corporation, either
# version 3.0 of the License, or (at your option) any later version.
#
# You should have received a copy of the CC-BY License along with this
# program.  If not, see <http://http://creativecommons.org/licenses/>.

"""Process HTML files replacing <swc-script> elements.
"""

import logging as _logging
import os as _os
import os.path as _os_path
import re as _re
import shlex as _shlex
import shutil as _shutil
import subprocess as _subprocess
import tempfile as _tempfile

try:  # Python 3
    import html.entities as _html_entities
except ImportError:  # Python 2
    import htmlentitydefs as _html_entities

_lxml_import_error = None
try:
    import lxml.etree as _etree
    import lxml.html as _lxml_html
except ImportError as e:
    _lxml_import_error = e
    import xml.etree.ElementTree as _etree

_LOG = _logging.getLogger('git-publish')
_LOG.addHandler(_logging.StreamHandler())
_LOG.setLevel(_logging.ERROR)

if _lxml_import_error is not None:
    _LOG.error('could not import lxml.etree: {}'.format(
            _lxml_import_error))
    _LOG.warning('falling back on xml.etree.ElementTree')


_ENTITY_REGEXP = _re.compile('&#?\w+;')

class ANSI (object):
    """ANSI color manipulation

    >>> ansi = ANSI()
    >>> ansi.csi.match('\x1b[01;32m').groups()
    ('01', '32')
    >>> ansi.csi.match('\x1b[01m').groups()
    ('01', None)
    >>> ansi.csi.match('\x1b[m').groups()
    (None, None)
    >>> e = _etree.Element('span', CLASS=('outside'))
    >>> text = u'\x1b[36m@@ -8,6 +8,10 @@\x1b[m \x1b[midea'
    >>> ansi._style_chunks(text)
    [({u'foreground': u'cyan'}, u'@@ -8,6 +8,10 @@'), (None, u' idea')]
    >>> e = ansi.parse(e, text)
    >>> print(_etree.tostring(e))
    <span CLASS="outside"><span style="color: cyan">@@ -8,6 +8,10 @@</span> idea</span>
    """
    # ANSI control sequence introducer
    csi = _re.compile('\x1b[[]([0-9]+)?;?([0-9]+)?m')
    colors = [
        u'black', u'red', u'green', u'yellow', u'blue', u'magenta', u'cyan',
        u'white']

    def parse(self, element, text):
        style_text = self._style_chunks(text)
        previous = element
        for style,text in style_text:
            if style:
                styles = []
                if u'weight' in style:
                    styles.append(u'font-weight: {}'.format(style[u'weight']))
                if u'foreground' in style:
                    styles.append(u'color: {}'.format(style[u'foreground']))
                if u'background' in style:
                    styles.append(
                        u'background-color: {}'.format(style[u'background']))
                style = '; '.join(styles)
                e = _etree.Element('span', style=style)
                e.text = text
                element.append(e)
                previous = e
            elif previous == element:
                element.text = text
            else:
                previous.tail = text
        return element

    def _style_chunks(self, text):
        style_text = []
        style = None
        previous = 0
        for match in self.csi.finditer(text):
            if match.start() > previous:
                style_text.append((style, text[previous:match.start()]))
            previous = match.end()
            style = self._select_graphic_rendition(match.groups())
        if previous < len(text):
            style_text.append((style, text[previous:]))
        i = 1
        while i < len(style_text):  # collapse unchanged styles
            previous_style,previous_text = style_text[i-1]
            style,text = style_text[i]
            if style == previous_style:
                style_text[i-1] = (style, previous_text + text)
                style_text.pop(i)
            else:
                i += 1
        return style_text

    def _select_graphic_rendition(self, parameters):
        if not parameters:
            return None  # default graphics
        ret = {}
        for parameter in parameters:
            if parameter is None:
                continue
            code = int(parameter)
            if code == 1:
                ret[u'weight'] = u'bold'
            elif code >= 30 and code <= 37:
                ret[u'foreground'] = self.colors[code - 30]
            elif code >= 40 and code <= 46:
                ret[u'background'] = self.colors[code - 40]
            else:
                raise NotImplementedError('ANSI graphics code {}'.format(code))
        if not ret:
            return None
        return ret


def CLASS(*args):  # class is a reserved word in Python
    return {'class': ' '.join(args)}


class User (object):
    """A user capable of executing commands
    """
    def __init__(self, username, homedir):
        self.username = username
        self.homedir = homedir
        self.cwd = homedir
        _LOG.debug('make {} home directory {}'.format(username, homedir))
        _os.makedirs(self.cwd)


class TemplateEnvironment (object):
    def __init__(self, prefix='', data_dir='.', encoding='utf-8'):
        self.prefix = prefix
        self.data_dir = data_dir
        self.encoding = encoding
        self.prompt = '$ '
        self.tmpdir = _tempfile.mkdtemp(prefix='software-carpentry-template-')
        self.users = {}
        self.ansi = ANSI()
        self.git_tick = 1112911993
        self.environ = dict(_os.environ)
        self.environ.update({
                'LANG': 'C',
                'LC_ALL': 'C',
                'PAGER': 'cat',
                'TERM': 'dumb',
                'TZ': 'UTC',
                'EDITOR': ':',
                })

    def cleanup(self):
        _shutil.rmtree(self.tmpdir)

    def eval(self, element):
        ret = []
        for child in element:
            if child.tag == '{}command'.format(self.prefix):
                ret.append(self.command(child))
            elif child.tag == '{}copy'.format(self.prefix):
                ret.append(self.copy(child))
            elif child.tag == '{}file'.format(self.prefix):
                ret.append(self.file(child.get('src')))
            elif child.tag == '{}newuser'.format(self.prefix):
                ret.append(self.newuser(child.text))
            else:
                raise NotImplementedError(child.tag)
        ret = self._squash_pre([e for e in ret if e is not None])
        if len(ret) == 0:
            return None
        elif len(ret) == 1:
            return ret[0]
        div = _etree.Element('div')
        for e in ret:
            div.append(e)
        return div

    def newuser(self, username):
        _LOG.info('newuser {}'.format(username))
        homedir = _os_path.join(self.tmpdir, 'home', username)
        self.users[username] = User(username=username, homedir=homedir)

    def command(self, element):
        username = element.get('user')
        user = self.users[username]
        command = (element.text or u'').strip()
        _LOG.info(u'command {}'.format(command))
        expect = int(element.get('expect', '0'))
        git_tick = element.get('git-tick', 'yes') == 'yes'
        display = element.get('display') or command
        if command:
            status,stdout,stderr = self._invoke(
                command, user, expect=(expect,), git_tick=git_tick)
        else:
            status = 0
            stdout_element = element.find('.//{}stdout'.format(self.prefix))
            if stdout_element is not None:
                stdout = stdout_element.text or u''
            else:
                stdout = u''
            stderr_element = element.find('.//{}stderr'.format(self.prefix))
            if stderr_element:
                stderr = stderr_element.text or u''
            else:
                stderr = u''
        if element.get('hidden', 'no') == 'yes':
            return
        pre = _etree.Element('pre')
        pre.text = '\n'
        prompt = _etree.Element('span', CLASS('out'))
        prompt.text = self.prompt
        pre.append(prompt)
        command_span = _etree.Element('span', CLASS('in'))
        command_span.text = display
        command_span.tail = '\n'
        pre.append(command_span)
        result = (stdout + stderr).replace(self.tmpdir, '').rstrip()
        if result:
            result_span = _etree.Element('span', CLASS('out'))
            result_span = self.ansi.parse(result_span, result)
            result_span.tail = '\n'
            pre.append(result_span)
        return pre

    def copy(self, element):
        source = self._path(element.get('src'))
        target = element.get('target')
        username = element.get('user')
        user = self.users[username]
        _LOG.info('copy "{}" to "{}" for "{}"'.format(
                source, target, username))
        _shutil.copy(source, _os_path.join(user.cwd, target))

    def file(self, path):
        path = self._path(path)
        _LOG.info(u'file "{}"'.format(path))
        pre = _etree.Element('pre')
        pre.text = u'\n{}'.format(
            unicode(open(path, 'rb').read(), self.encoding))
        return pre

    def _invoke(self, command, user, expect=(0,), git_tick=True):
        _LOG.info(u'execute "{}" as {}'.format(command, user.username))
        cmds = [unicode(x, 'utf-8')
                for x in _shlex.split(command.encode('utf-8'))]
        _LOG.debug(u'split into {}'.format(cmds))
        for i,arg in enumerate(cmds):
            if i > 0 and arg.startswith(u'~'):
                path = self._expanduser(arg, user=user)
                _LOG.debug(u'expand argument {} from {} to {}'.format(
                        i, arg, path))
                cmds[i] = path
        self.environ['GIT_COMMITTER_DATE'] = '{} -0700'.format(self.git_tick)
        self.environ['GIT_AUTHOR_DATE'] = self.environ['GIT_COMMITTER_DATE']
        if cmds[0] == u'cd':
            stdout = stderr = ''
            status = 0
        else:
            assert _os_path.isdir(user.cwd), user.cwd
            p = _subprocess.Popen(
                cmds, stdout=_subprocess.PIPE, stderr=_subprocess.PIPE,
                cwd=user.cwd, shell=False, env=self.environ)
            stdout,stderr = p.communicate()
            status = p.wait()
        if status not in expect:
            raise ValueError((command, stdout, stderr, status, expect))
        stdout = unicode(stdout, self.encoding)
        if cmds[0] == u'cd':
            user.cwd = _os_path.join(user.cwd, cmds[-1])
            assert _os_path.isdir(user.cwd), user.cwd
            _LOG.info(u'user {} changing directory to {}'.format(
                    command, user.cwd))
        elif (git_tick and
              status == 0 and
              cmds[0] == u'git' and
              cmds[1] in [u'commit', u'merge']):
            self.git_tick += 60
            _LOG.debug(u'git tick')
        _LOG.info(u'executed "{}" as {}'.format(command, user.username))
        return (status, stdout, stderr)

    def _path(self, path):
        """Return a path to a data file
        """
        data_path = _os_path.join(self.data_dir, path) 
        for p in [path, data_path]:
            if _os_path.exists(p):
                return p
        return path

    def _expanduser(self, path, user):
        """Shell-style user expansion

        >>> e = TemplateEnvironment()
        >>> e.newuser('jdoe')
        >>> e.newuser('jane')
        >>> jdoe = e.users['jdoe']
        >>> e._expanduser('~', user=jdoe)  # doctest: +ELLIPSIS
        '/tmp/software-carpentry-template-.../home/jdoe'
        >>> e._expanduser('~jane/', user=jdoe)  # doctest: +ELLIPSIS
        '/tmp/software-carpentry-template-.../home/jane/'
        >>> e._expanduser('~/a/b/c', user=jdoe)  # doctest: +ELLIPSIS
        '/tmp/software-carpentry-template-.../home/jdoe/a/b/c'
        >>> e.cleanup()
        """
        base_tail = path.split(_os_path.sep, 1)
        base = base_tail[0]
        tail = base_tail[1:]
        if base == '~':
            return _os_path.join(user.homedir, *tail)
        elif base.startswith('~'):
            username = base[1:]
            u = self.users[username]
            return _os_path.join(u.homedir, *tail)
        return path

    def _squash_pre(self, elements):
        i = 1
        while i < len(elements):
            if elements[i-1].tag == 'pre' and elements[i].tag == 'pre':
                for c in elements[i]:  # merge into previous <pre> block
                    elements[i-1].append(c)
                elements[i-1].tail = elements[i].tail
                elements.pop(i)
            else:
                i += 1
        return elements


def parse_template(template, data_dir='.', prefix='swc-'):
    """Takes template path and path to data directory
    """
    environment = TemplateEnvironment(prefix=prefix, data_dir=data_dir)
    try:
        for element in template.findall('.//{}script'.format(prefix)):
            _LOG.debug(_etree.tostring(element).rstrip())
            new_element = environment.eval(element)
            parent = getparent(template, element)
            if new_element is None:
                getprevious(template, element).tail += element.tail
                parent.remove(element)
            else:
                new_element.tail = element.tail
                replace(parent, element, new_element)
    finally:
        environment.cleanup()

# utitily functions

def _entity_replace(match):
    """Replace a single _ENTITY_REGEXP match

    Based on Fredrik Lundh's example:
    http://effbot.org/zone/re-sub.htm#unescape-html
    """
    text = match.group(0)
    if text.startswith('&#'):  # character reference
        try:
            if text.startswith('&#x'):
                return unichr(int(text[3:-1], 16))
            else:
                return unichr(int(text[2:-1]))
        except ValueError:
            pass
    else:  # named entity
        try:
            text = unichr(_html_entities.name2codepoint[text[1:-1]])
        except KeyError:
            pass
    return text  # leave as is

def unescape(text):
    """Unescape HTML entities

    >>> unescape('&lt;&gt;')
    '<>'
    >>> unescape('&euml;')
    u'\\xeb'
    """
    if _lxml_import_error is None:
        return _lxml_html.fromstring(text).text
    else:
        _ENTITY_REGEXP.sub(_entity_replace, text)

# lxml.etree compatibility functions for xml.etree.ElementTree

def getparent(root, element):
    if hasattr(element, 'getparent'):  # lxml.etree
        return element.getparent()
    else:  #xml.etree.ElementTree
        for node in root.iter():
            if element in node:
                return node
        raise ValueError((root, element))

def getprevious(root, element):
    if hasattr(element, 'getprevious'):  # lxml.etree
        return element.getprevious()
    else:  #xml.etree.ElementTree
        parent = getparent(root, element)
        previous = None
        for node in parent:
            if node == element:
                return previous
            previous = node

def replace(parent, old, new):
    if hasattr(parent, 'replace'):  # lxml.etree
        return parent.replace(old, new)
    else:  #xml.etree.ElementTree
        index = list(parent).index(old)
        parent.remove(old)
        parent.insert(index, new)


class EntityMapper (object):
    """No-op mapper to avoid "unknown XML entities" errors
    """
    def __getitem__(self, key):
        return key


if __name__ == '__main__':
    import argparse as _argparse

    parser = _argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '-v', '--verbose', default=0, action='count',
        help='increment verbosity')
    parser.add_argument(
        'template', metavar='PATH', nargs='+', help='template file')

    args = parser.parse_args()

    if args.verbose:
        _LOG.setLevel(max(_logging.DEBUG, _LOG.level - 10*args.verbose))

    for path in args.template:
        _LOG.info('process {}'.format(path))
        target_path = path
        base_dir,filename = _os_path.split(path)
        base_file,extension = _os_path.splitext(filename)
        data_dir = _os_path.join(base_dir, 'src', base_file)
        if _lxml_import_error is None:
            parser = _etree.XMLParser(resolve_entities=False)
        else:
            parser = _etree.XMLParser()
            parser.entity = EntityMapper()
        tree = _etree.parse(path, parser)
        root = tree.getroot()
        parse_template(root, data_dir=data_dir)
        tree.write(target_path)
