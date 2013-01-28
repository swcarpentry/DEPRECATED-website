import jinja2

loader = jinja2.FileSystemLoader(['.'])
environment = jinja2.Environment(loader=loader)
template = environment.get_template('biography.html')

result = template.render(name='Beatrice Tinsley',
                         facts=['Born 1941',
                                'Died 1981',
                                'Studied stellar aging'])
print result

result = template.render(name='Helen Sawyer Hogg',
                         facts=['Born 1905',
                                'Died 1993',
                                'Studied globular clusters',
                                'Wrote a popular astronomy column for 30 years'])
print result
