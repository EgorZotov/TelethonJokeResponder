import requests
import json
import time
import urllib.parse
import hashlib
import os
from dotenv import load_dotenv
load_dotenv()

def get_porutchik_joke():
    skey = os.getenv("JOKES_SECRET_KEY")
    joke_request = {
        'pid':os.getenv("JOKES_PID"),   
        'method': 'getRandItemP',               
        'format':'json',                 
        'charset':'utf-8',
        'series': 5,
        'uts': int(time.time()),                                        
    }
    url_encoded_joke_request = urllib.parse.urlencode(joke_request)
    utf_encoded_sig = (url_encoded_joke_request+skey).encode('utf-8')
    request_hash = hashlib.md5(utf_encoded_sig).hexdigest(); 
    print(request_hash)
    joke_request["hash"] = request_hash
    print(joke_request)
    url = 'http://anecdotica.ru/api'
    r = requests.get(url, params = joke_request)
    joke_response = json.loads(r.content)
    joke_text = joke_response['item']['text']
    print(joke_text)
    return joke_text