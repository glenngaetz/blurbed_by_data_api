from apiclient import APIClient
from datetime import datetime
import pprint

pp = pprint.PrettyPrinter(indent=4)


"""
Load some initial publisher lists for testting.
"""

client = APIClient('test', 'test', 'http://localhost:8000')


# Test some POST requests
urls = [
    'https://publishers.ca',
    'https://books.bc.ca/who-we-are/member-directory/',
]
for url in urls:
    web_resource = client.get('web_resource', data={
        'url': url,
        'resource_type': 'publisher_list',
    })
    if web_resource:
        print('WebResource to be updated:')
        pp.pprint(web_resource)
        web_resource = client.patch('web_resource', data={
            'verified': datetime.now(),
            'verified_by': 'admin',
            'modified_by': 'admin',
            'id': web_resource['id'],
        })
        print('WebResource updated:')
        pp.pprint(web_resource)
