import sys
import xml.etree.ElementTree as ET

doc = ET.parse(sys.argv[1])
root = doc.getroot()
atoms = root.findall('.//atom')
count = {}
for a in atoms:
    symbol = a.attrib['symbol']
    if symbol in count:
        count[symbol] += 1
    else:
        count[symbol] = 1
print count
