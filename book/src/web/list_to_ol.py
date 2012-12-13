import xml.etree.ElementTree as ET

def convert(values):
    '''Convert a list of values to an <ol> list.'''

    result = ET.Element('ol')
    for v in values:
        ET.SubElement(result, 'li').text = str(v)
    return result

root = convert([1, "two", 3.4])
print ET.tostring(root)
