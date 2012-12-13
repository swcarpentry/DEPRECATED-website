import xml.etree.ElementTree as ET

root = ET.Element('html')

body = ET.Element('body')
root.append(body)

title = ET.SubElement(body, 'h1')
title.text = 'Dimorphism'

p1 = ET.SubElement(body, 'p')
p1.attrib['class'] = 'definition'
p1.text = 'Occurring or existing in two different '
u = ET.SubElement(p1, 'u')
u.text = 'forms'
u.tail = '.'

long_text = '''The most notable form is sexual dimorphism,
in which males and females have noticeably different appearances.'''
ET.SubElement(body, 'p').text = long_text

print ET.tostring(root)
