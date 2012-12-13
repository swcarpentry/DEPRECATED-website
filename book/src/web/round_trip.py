import xml.etree.ElementTree as ET

original = '''<root><node
                     front="1"
                     back="2">content</node></root>'''

doc = ET.fromstring(original)
print ET.tostring(doc, 'utf-8')
