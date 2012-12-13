import sys
import requests
import xml.etree.ElementTree as ET

def main(args):
    first_country = 'AUS'
    second_country = 'CAN'
    if len(args) > 0:
        first_country = args[0]
    if len(args) > 1:
        second_country = args[1]
    ratios(first_country, second_country)

def ratios(first_country, second_country):
    '''Show ratio of average temperatures for two countries over time.'''
    first = get_temps(first_country)
    second = get_temps(second_country)
    assert len(first) == len(second), 'Length mis-match in results'
    keys = first.keys()
    keys.sort()
    for k in keys:
        print k, first[k] / second[k]

def get_temps(country_code):
    '''Get annual temperatures for a country.'''
    doc = get_xml(country_code)
    result = {}
    for element in doc.findall('domain.web.V1WebCru'):
        year = find_one(element, 'year').text
        temp = find_one(element, 'data').text
        result[int(year)] = kelvin(float(temp))
    return result

def get_xml(country_code):
    '''Get XML temperature data for a country.'''
    url = 'http://climatedataapi.worldbank.org/climateweb/rest/v1/country/cru/tas/year/%s.XML'
    u = url % country_code
    response = requests.get(u)
    doc = ET.fromstring(response.text)
    return doc

def find_one(node, pattern):
    '''Get exactly one child that matches an XPath pattern.'''
    all_results = node.findall(pattern)
    assert len(all_results) == 1, 'Got %d children instead of 1' % len(all_results)
    return all_results[0]

def kelvin(celsius):
    '''Convert degrees C to degrees K.'''
    return celsius + 273.15

if __name__ == '__main__':
    main(sys.argv[1:])
