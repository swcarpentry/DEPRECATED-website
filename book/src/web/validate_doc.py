import xml.etree.ElementTree as ET

doc = ET.parse('bad_formulas.xml')
all_atoms = doc.findall('.//atom')
proper_atoms = doc.findall('.//formula/atom')
wrongly_placed = set(all_atoms) - set(proper_atoms)
for atom in wrongly_placed:
    print ET.tostring(atom)
