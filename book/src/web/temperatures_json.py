import sys
import urllib2
import json

def kelvin(celsius):
    '''Convert degrees C to degrees K.'''
    return celsius + 273.15

def get_temps(country_code):
    '''Get annual temperatures for a country.'''
    url = 'http://climatedataapi.worldbank.org/climateweb/rest/v1/country/cru/tas/year/%s'
    u = url % country_code
    connection = urllib2.urlopen(u)
    raw = connection.read()
    structured = json.loads(raw)
    connection.close()
    result = {}
    for entry in structured:
        year, celsius = entry['year'], entry['data']
        result[year] = kelvin(celsius)
    return result

def main(first_country, second_country):
    '''Show ratio of average temperatures for two countries over time.'''
    first = get_temps(first_country)
    second = get_temps(second_country)
    assert len(first) == len(second), 'Length mis-match in results'
    keys = first.keys()
    keys.sort()
    for k in keys:
        print k, first[k] / second[k]

if __name__ == '__main__':
    first_country = 'AUS'
    second_country = 'CAN'
    if len(sys.argv) > 1:
        first_country = sys.argv[1]
    if len(sys.argv) > 2:
        second_country = sys.argv[2]
    main(first_country, second_country)
