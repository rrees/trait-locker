import os
import requests

_ROOT_URL = 'https://jsonbin.org/rrees/trait-locker'

_API_KEY = os.environ.get('JSONBIN_API_KEY', None)

def headers():
    return {
        'Authorization': f'token {_API_KEY}'
    }

def read():

    response = requests.get(_ROOT_URL, headers=headers())

    print(response.status_code)
    if response.status_code == 200:
        return response.json()
    
    return None

def write(bundle):

    bundle_id = bundle.get('id')
    store = read()

    payload= {
        bundle_id: bundle,
    }

    if not store:
        response = requests.post(_ROOT_URL,
            headers=headers(),
            json=payload)
        
        if response.status_code == 200:
            return response.json()

        return None
    
    response = requests.patch(
        _ROOT_URL,
        headers=headers(),
        json=payload,
    )

    if response.status_code == 200:
        return response.json()
    
    return None



