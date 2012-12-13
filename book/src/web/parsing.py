import sys
from cStringIO import StringIO
from xml.etree import ElementTree as ET
from htmlentitydefs import name2codepoint

source = StringIO("""<html>
<body>
<p>Less than "&lt;"</p>
<p>Non-breaking space "&nbsp;"</p>
</body>
</html>""")

parser = ET.XMLParser()
parser.parser.UseForeignDTD(True)
parser.entity.update((x, unichr(i)) for x, i in name2codepoint.iteritems())
etree = ET.ElementTree()

tree = etree.parse(source, parser=parser)
for p in tree.findall('.//p'):
     print ET.tostring(p, encoding='UTF-8')
