import sys
import os
from datetime import date
import jinja2
import json
from temperatures import get_temps

INDIVIDUAL_PAGE = 'temp_ratio.html'
INDEX_PAGE = 'index.html'
INDEX_FILE = 'index.json'

def main(args):
    '''
    Create web page showing temperature ratios for two countries,
    and update the index.html page with the new entry.
    '''

    assert len(args) == 4, \
           'Usage: make_indexed_page template_dir output_dir country_1 country_2'
    template_dir = args[0]
    output_dir = args[1]
    country_1 = args[2]
    country_2 = args[3]
    the_date = date.isoformat(date.today())

    loader = jinja2.FileSystemLoader([template_dir])
    environment = jinja2.Environment(loader=loader)

    page = make_page(environment, country_1, country_2, the_date)
    save_page(output_dir, '%s-%s.html' % (country_1, country_2), page)

    index_data = load_index(output_dir, INDEX_FILE)
    index_data['entries'].append([country_1, country_2, the_date])
    save_page(output_dir, INDEX_FILE, json.dumps(index_data))

    page = make_index(environment, index_data)
    save_page(output_dir, INDEX_PAGE, page)

def make_page(environment, country_1, country_2, the_date):
    '''Create page showing temperature ratios.'''

    data_1 = get_temps(country_1)
    data_2 = get_temps(country_2)
    years = data_1.keys()
    years.sort()

    template = environment.get_template(INDIVIDUAL_PAGE)
    result = template.render(country_1=country_1, data_1=data_1,
                             country_2=country_2, data_2=data_2,
                             years=years, the_date=the_date)

    return result

def load_index(output_dir, filename):
    '''Load index data from output_dir/filename.'''

    path = os.path.join(output_dir, filename)
    reader = open(path, 'r')
    result = json.load(reader)
    reader.close()
    return result

def make_index(environment, index_data):
    '''Refresh the HTML index page.'''

    template = environment.get_template(INDEX_PAGE)
    return template.render(updated=index_data['updated'],
                           entries=index_data['entries'])

def save_page(output_dir, page_name, content):
    '''Save text in a file output_dir/page_name.'''

    path = os.path.join(output_dir, page_name)
    writer = open(path, 'w')
    writer.write(content)
    writer.close()

if __name__ == '__main__':
    main(sys.argv[1:])
