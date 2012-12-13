import xml.etree.ElementTree as ET

source = '''<formulas>
  <formula name="ammonia">
    <atom symbol="N" number="1"/>
    <atom symbol="H" number="3"/>
  </formula>
  <atom symbol="H" number="2"/>       <!-- mistake! -->
  <formula name="water">
    <atom symbol="O" number="1">
      <atom symbol="H" number="2"/>   <!-- another mistake -->
    </atom>
  </formula>
</formulas>'''

doc = ET.fromstring(source)
all_atoms = doc.findall('.//atom')
proper_atoms = doc.findall('.//formula/atom')
wrongly_placed = set(all_atoms) - set(proper_atoms)
for atom in wrongly_placed:
    print ET.tostring(atom)
