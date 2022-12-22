import requests
import json
from urllib.parse import urljoin
import pprint

pp = pprint.PrettyPrinter(indent=4)


class APIClient:

    def __init__(self, user, pwd, host):
        self.user = user
        self.pwd = pwd
        self.host = host
        self.token = ''

        data = {
            'username': user,
            'password': pwd,
        }

        response = requests.get(urljoin(host, '/user/auth'), data=data)
     
        print('Response:')
        print(response.status_code)
        print(response.headers['content-type'])
        pp.pprint(response.json())        

        data = response.json()
        token = data['user'][0]['token']

    def get(self, model, args={}, data={}):
        print(f'model: {model}')
        url = urljoin(self.host, model)
        try:
            url = urljoin(self.host, model, str(args['id']))
        except KeyError:
            pass
       
        headers = {'Authorization': f'Bearer {self.token}'}
        response = requests.get(url, headers=headers, data=data) 

        data = response.json()
      
        if 'queue' in model:
            model = 'web_resource'
            try:
                return data[model]
            except KeyError:
                return None
        
        try:
            if len(data[model]) == 1:
                return data[model][0]
            elif len(data[model]) > 1:
                return data[model]
            else:
                return None
        except KeyError:
            return None

    def post(self, model, data={}):

        url = urljoin(self.host, model)

        headers = {'Authorization': f'Bearer {self.token}'}

        data['added_by'] = self.user
        response = requests.post(url, headers=headers, data=data)

        data = response.json()

        try: 
            if len(data[model]) == 1:
                return data[model][0]
            elif len(data[model]) > 1:
                return data[model]
            else:
                return None
        except KeyError:
            return None

    def patch(self, model, data={}):

        url = urljoin(self.host, model)

        headers = {'Authorization': f'Bearer {self.token}'}

        response = requests.patch(url, headers=headers, data=data)

        data = response.json()

        try:
            if len(data[model]) == 1:
                return data[model][0]
            elif len(data[model]) > 1:
                return data[model]
            else:
                return None
        except KeyError:
            return None

    def delete(self, model, data={}):

        url = urljoin(self.host, model)

        headers = {'Authorization': f'Bearer {self.token}'}

        response = requests.delete(url, headers=headers, data=data)
        return response.status_code == 200
