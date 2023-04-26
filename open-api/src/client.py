import requests
import logging

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def printAndLog(logging, text):
    print(text)
    logging(text)

class RadioClient(object):
    def __init__(self, base_uri):
        self.base_uri = base_uri

    def get_radio(self, user_name):
        """Fetch radio station stats from the server."""
        
        uri = self.base_uri + '/json/stats'
        printAndLog(logging.info, "Fetching: " + uri)
        response = requests.get(uri)
        printAndLog(logging.info, "Status: " + str(response.status_code))
        if response.status_code == 404:
            return None
        return response.json()
    
