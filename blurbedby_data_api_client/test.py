from apiclient import APIClient

import pprint

pp = pprint.PrettyPrinter(indent=4)

"""
This needs real tests, but it works for now
"""

client = APIClient('test', 'test', 'http://localhost:8000')


# Test some GET requests
r = client.get('web_resource')
print('WebResources:')
pp.pprint(r)

r = client.get('web_resource', args={'id':1})
print('WebResources:')
pp.pprint(r)

r = client.get('book')
print('Books:')
pp.pprint(r)

r = client.get('book', args={'id':3})
print('Book 3:')
pp.pprint(r)

book_list = client.get('book', data={
    'added__daterange': ['2022-9-03', '2022-09-04']
})
print('Books added in date range')
print(f'number: {len(book_list)}')
pp.pprint(book_list)

blurb_list = client.get('blurb', data={
    'book_id': 2,
})
print(f'Blurbs for book 2:')
pp.pprint(blurb_list)

scrape_log_list = client.get('scrape_log', data={
    'scrape_state': ['fail'],
})
print('ScrapeLog entries:')
pp.pprint(scrape_log_list)

# Test some POST requests
web_resource = client.post('web_resource', data={
    'url': 'https://arsenalpulp.com/',
    'title': 'Arsenal Pulp Press',
    'resource_type': 'publisher_site',
})
if web_resource:
    print('WebResource added:')
    pp.pprint(web_resource)

# Test some PATCH requests
web_resource = client.get('web_resource', data={
    'url': 'https://arsenalpulp.com/',
})
updated_web_resource = client.patch('web_resource', data={
    'id': web_resource['id'],
    'Title': 'Arsenal Pulp',
})
print('WebResource updated:')
pp.pprint(web_resource)

# Test the queue
queue = client.get('queue', data={
    'resource_type': 'publisher_list',
})
print('Queue:')
pp.pprint(queue);

# Clean up the added items
web_resource = client.get('web_resource', data={
    'url': 'https://arsenalpulp.com/',
})
result = client.delete('web_resource', data={
    'id': web_resource['id'],
})
print('Deleted:')
pp.pprint(result)

