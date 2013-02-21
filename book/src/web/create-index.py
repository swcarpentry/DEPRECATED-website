import json

index_data = {
    'updated' : '2013-05-09',
    'entries' : [
        ['AUS', 'CAN', '2013-03-07'],
        ['AUS', 'NOR', '2013-03-09'],
        ['CAN', 'NOR', '2013-04-22'],
        ['CAN', 'MDG', '2013-05-09']
    ]
}

writer = open('index.json', 'w')
json.dump(index_data, writer)
writer.close()
