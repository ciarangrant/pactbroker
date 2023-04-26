"""pact test for user service client"""

import json
import logging
import os
import sys
import datetime
import configparser
import pytest
import requests

from src.client import RadioClient
from pact import Consumer, Like, Provider, Term, Format

#check we are in the tests folder when running pytest
if os.path.basename(os.getcwd()) != 'tests':
    print('*** Run `pytests -s` from the `tests` folder ***')
    sys.exit()

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

publish_pact = True
verify_pact = True
version = datetime.datetime.now().strftime("%d%m%y%H%M")

PACT_FILE = "RadioBrowserclient-RadioBrowser.json"
PACT_UPLOAD_URL = ("http://localhost:9292/pacts/provider/RadioBrowser/consumer/RadioBrowserClient/version")
PACT_BROKER_BASE_URL="http://localhost:9292/"
PACT_BROKER_TOKEN="g0wWA7F8Ip5SYI3l2z4HEA"
PACT_MOCK_HOST = 'localhost'
PACT_MOCK_PORT = 1234
PACT_DIR = os.path.dirname(os.path.realpath(__file__))


def printAndLog(logging, text):
    print(text)
    logging(text)

@pytest.fixture
def client():
    return RadioClient(
        'http://{host}:{port}'
        .format(host=PACT_MOCK_HOST, port=PACT_MOCK_PORT)
    )

def validate_date(date_text):
    res = True
    # using try-except to check for truth value
    try:
        res = bool(datetime.datetime.strptime(date_text, '%Y-%m-%dT%H:%M:%S'))
    except ValueError:
        res = False

    return res

def push_to_broker(version):
    """TODO: see if we can dynamically learn the pact file name, version, etc."""
    with open(os.path.join(PACT_DIR, PACT_FILE), 'rb') as pact_file:
        pact_file_json = json.load(pact_file)

    
    auth_token = "Bearer "+PACT_BROKER_TOKEN
    headers = {"Authorization": auth_token}

    printAndLog(logging.info, "Uploading pact file to pact broker - version: " + version)
    
    r= requests.put(
        "{}/{}".format(PACT_UPLOAD_URL,version),
        json=pact_file_json
        ,headers=headers
    )

    if not r.ok:
        logging.error("Error uploading: %s", r.content)
        r.raise_for_status()
    else:
        printAndLog(logging.info,"Successfully Uploading pact file to pact broker - version: " + version)    


@pytest.fixture(scope='session')
def pact(request):
    pact = Consumer('RadioBrowserClient', branch='main').has_pact_with(
        Provider('RadioBrowser'), host_name=PACT_MOCK_HOST, port=PACT_MOCK_PORT,
        pact_dir=PACT_DIR)
    pact.start_service()
    yield pact
    pact.stop_service()
    
    if not request.node.testsfailed and publish_pact:
        printAndLog(logging.info, '*** Publishing Pact ***')
        push_to_broker(version)

    if not request.node.testsfailed and verify_pact:
        printAndLog(logging.info, '*** Verifying Pact ***')
        try:
            parent_path = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
            verify = os.system(parent_path + '/verify_pact.sh ' + version)  
            if verify == 0:
                printAndLog(logging.info,"Successfully verified pact file on pact broker - version: " + version)   
            else:
                printAndLog(logging.info,"Failed to verify pact file on pact broker - version: " + version)   
        except:
            printAndLog(logging.info,"Failed to verify pact file on pact broker - version: " + version)

    config = configparser.ConfigParser()
    logPath = os.getcwd() + '/'
    iniFile = logPath + 'pytest.ini'
    config.read(iniFile)
    printAndLog(logging.info,'Log file = ' + logPath + config['pytest']['log_file']) 


def test_get_radio(pact, client):
    expected = {
        'countries': 212
    }

    (pact
     .given('Country stats exist')
     .upon_receiving('a request for country stats')
     .with_request('get', '/json/stats')
     .will_respond_with(200, body=Like(expected)))

    with pact:
        result = client.get_radio('')

    printAndLog(logging.info, result)
    printAndLog(logging.info, expected)
    assert result == expected

    # assert something with the result, for ex, did I process 'result' properly?
    # or was I able to deserialize correctly? etc.

def test_integer_fields(pact, client):
    expected = {
        'supported_version': Format().integer,
        'stations': Format().integer
    }

    (pact
     .given('Country stats exist with integer fields')
     .upon_receiving('a request for country stats with integer fields')
     .with_request('get', '/json/stats')
     .will_respond_with(200, body=Like(expected)))

    with pact:
        result = client.get_radio('')

    printAndLog(logging.info, result)
    printAndLog(logging.info, expected)
    assert isinstance(result['supported_version'], int) 

    # assert something with the result, for ex, did I process 'result' properly?
    # or was I able to deserialize correctly? etc.