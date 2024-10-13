import requests
from aptoswallet.functions import account_info,token_info

URL = "https://api.mainnet.aptoslabs.com/v1/"

def request(url):
    response = requests.get(url)
    if response.status_code == 200:
        resources = response.json()
        return resources