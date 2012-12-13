import sys
from temperatures import get_temps
from datetime import date

def main(args):
    first_country = 'AUS'
    second_country = 'CAN'
    index_page = 'index.html'
    if len(args) > 0:
        first_country = args[0]
    if len(args) > 1:
        second_country = args[1]
    if len(args) > 2:
        index_page = args[2]
    make_page(sys.stdout, first_country, second_country)
    update_index(index_page, first_country, second_country)

def make_page(output, first_country, second_country):
    '''Create page showing temperature ratios.'''

    first_data = get_temps(first_country)
    second_data = get_temps(second_country)

    the_date = date.isoformat(date.today())

    html = ET.Element('html')
    head = ET.SubElement(html, 'head')
    revised = ET.SubElement(head, 'meta', {'name'    : 'revised',
                                           'content' : the_date})

    body = ET.SubElement(html, 'body')
    h1 = ET.SubElement(body, 'h1')
    h1.text = 'Ratio of Average Annual Temperatures for %s and %s' % \
              (first_country, second_country)

    make_table(body, first_data, second_data)

    output.write(ET.tostring(html))

def make_table(parent, first_data, second_data):
    '''Create table in page showing temperature ratios.'''
    table = ET.SubElement(parent, 'table')
    table.attrib['class'] = 'data'
    keys = first_data.keys()
    keys.sort()
    for year in keys:
        tr = ET.SubElement(table, 'tr')
        td_year = ET.SubElement(tr, 'td', {'class' : 'year'})
        td_year.text = str(year)
        td_data = ET.SubElement(tr, 'td', {'class' : 'data'})
        td_data.text = str( first_data[year] / second_data[year] )

def update_index(path_to_index, first_country, second_country):
    '''Update the index of our data files.'''

    the_date = date.isoformat(date.today())
    doc = ET.parse(path_to_index)

    replace_meta(doc, the_date)
    add_record(doc, the_date, first_country, second_country)

    writer = open(path_to_index, 'w')
    writer.write(ET.tostring(doc))

if __name__ == '__main__':
    main(sys.argv[1:])
