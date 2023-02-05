import requests
from auth import http_auth
import loggy
from pathlib import Path
from inspect import stack
from requests.auth import HTTPBasicAuth
from http.client import HTTPConnection
from pprintpp import pprint as pp
from dataclasses import dataclass, field
import json
import os

script_name = Path(__file__).stem
logger = loggy.logging.getLogger(script_name)

headers = {
    'Content-Type': 'application/json'
}

url=os.getenv("FS_API_URL",'')

@dataclass
class GetResults():
    status_code: int
    results: list=field(default_factory=list)



def _get(path: str=None, params: dict=None, auth=http_auth, headers: dict=headers)->requests.Response:
    uri=f'{url}{path}'
    logger.debug(f"caller: {stack()[1].function}, Getting {uri}")
    return requests.get(uri, auth=auth, params=params, headers=headers)

def get_freshservice(path: str=None, params: dict={}, headers: dict=headers, no_page: bool=False):
    page_number = 1
    if not no_page:
        params['per_page']=100
        params['page']=1
    pag_list = []
    status_code = None
    autho=http_auth
    while True:
        done=None
        pagination = _get(path=path, params=params, auth=autho, headers=headers)
        logger.debug(f"Trying {path}, Page: {page_number}")
        try:
            content = pagination.json()
        except Exception as e:
            logger.error(f"Failed to decode JSON. {pagination.content}")
            content = {}
            done=True
        if content:
            for item in content:
                if not content[item]:
                    done=True
                    break
        status_code = pagination.status_code
        if done:
            break
        pag_list.append(content)
        if not no_page:
            params['page']+=1
            page_number +=1
        
        if no_page:
            break
    return GetResults(status_code, pag_list)
        
        
    


def post_freshservice(path: str=None, headers: dict=headers, data: dict=None)->requests.Response:
    uri=f'{url}{path}'
    autho=http_auth
    HTTPConnection.debuglevel = 1
    logger.debug(f'caller: {stack()[1].function}, Postting {uri} :: {data}')
    return requests.post(uri, auth=autho, headers=headers, json=data)

def put_freshservice(path: str=None, headers: dict=headers, data: dict=None)->requests.Response:
    uri=f'{url}{path}'
    logger.debug(f'caller: {stack()[1].function}, Putting {uri} :: {data}')
    autho=http_auth
    HTTPConnection.debuglevel = 1
    return requests.put(uri, auth=autho, headers=headers, json=data)