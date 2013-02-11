import sys
import jinja2
from temperatures import get_temps
from datetime import date

def main(args):
    '''Create web page showing temperature ratios for two countries.'''

    assert len(args) == 4, \
           'Usage: make_data_page template_filename output_filename country_1 country_2'
    template_filename = args[0]
    output_filename = args[1]
    country_1 = args[2]
    country_2 = args[3]

    page = make_page(template_filename, country_1, country_2)

    writer = open(output_filename, 'w')
    writer.write(page)
    writer.close()

def make_page(template_filename, country_1, country_2):
    '''Create page showing temperature ratios.'''

    data_1 = get_temps(country_1)
    data_2 = get_temps(country_2)
    years = data_1.keys()
    years.sort()
    the_date = date.isoformat(date.today())

    loader = jinja2.FileSystemLoader(['.'])
    environment = jinja2.Environment(loader=loader)
    template = environment.get_template(template_filename)
    result = template.render(country_1=country_1, data_1=data_1,
                             country_2=country_2, data_2=data_2,
                             years=years, the_date=the_date)

    return result

if __name__ == '__main__':
    main(sys.argv[1:])
