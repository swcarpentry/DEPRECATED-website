import requests
import xml.etree.ElementTree as ET

INDEX_URL = 'http://my.site/tempratio/index.html'

def main(args):
    '''Main driver for program.'''

    assert len(args) == 2
    url, filename = args

    current_index = get_web(url)
    old_index = get_file(filename)

    new_index = current_index - old_index
    show_index(new_index)

    save_index(filename, current_index)

def get_web(url):
    '''Get index from a URL on the web.'''
    response = requests.get(INDEX_URL)
    doc = ET.fromstring(response.text)
    return parse_index(doc)

def get_file(filename):
    '''Get index from a file on disk.'''
    reader = open(filename, 'r')
    data = reader.read()
    reader.close()
    doc = ET.fromstring(data)
    return parse_index(doc)

def show_index(index):
    '''Display index in order.'''
    temp = sorted(index)
    for (date, country_a, country_b) in temp:
        print date, country_a, country_b

def save_index(filename, index):
    '''Save index as XML for next time.'''
    writer = open(filename, 'w')
    writer.write(ET.tostring(index))
    writer.close()

def parse_index(doc):
    '''Get a set of (date, country_a, country_b) tuples from an index file.'''
    index = set()
    rows = doc.findall('.//table[@class="data"]/tr')
    for r in rows:
        the_date = r.findall('./td[@class="revised"]')[0].text
        the_countries = r.findall('./td[@class="country"]')
        country_a = the_countries[0].text
        country_b = the_countries[1].text
        new_entry = (the_date, country_a, country_b)
        index.add(new_entry)
    return index

if __name__ == '__main__':
    main(sys.argv[1:])
