import xml.etree.ElementTree as ET

page = '''<html>
  <body>
    <h1>Dimorphism</h1>
    <p class="definition">Occurring or existing in two different <u>forms</u>.</p>
    <p>
      The most notable form is sexual dimorphism,
      in which males and females have noticeably different appearances.
    </p>
  </body>
</html>'''

doc = ET.fromstring(page)
text = ET.tostring(doc, 'utf-8')
print text
