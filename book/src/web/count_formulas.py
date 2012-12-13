import sys
import xml.etree.ElementTree as ET

doc = ET.parse(sys.argv[1])
root = doc.getroot()
formulas = root.findall("./formula")
print len(formulas)
