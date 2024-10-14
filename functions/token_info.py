from aptoswallet.comon.res import *

def token_info_search(address):
    url = URL+f'accounts/{address}/resources'
    resources = request(url)
    for resource in resources:
        event_type = resource.get("type", "")
        if "CoinInfo" in event_type:
            data = resource.get("data", {})
            decimals = data.get('decimals')
            return decimals


def get_remaining_tokens(token_address, address):
    url = URL + f"/accounts/{address}/resource/0x1::coin::CoinStore<{token_address}>"
    response = request(url)
    if isinstance(response, dict):
        data = response.get('data', {})
        if 'coin' in data:
            remaining = data['coin'].get('value', 0)
            return int(remaining)
        else:
            return 0
    else:
        return "Erreur: La réponse n'est pas un dictionnaire valide"


def get_token_price(address):
    url = f"https://api.dexscreener.com/latest/dex/tokens/{address}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if 'pairs' in data:
            for pair in data['pairs']:
                if pair['baseToken']['address'] == address or pair['quoteToken']['address'] == address:
                    price = pair['priceUsd']
                    return float(price)

    except requests.exceptions.RequestException as e:
        return f"Erreur lors de la récupération du prix : {e}"

def get_token_info(token_address,address):
    url = f"https://api.dexscreener.com/latest/dex/tokens/{token_address}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        url = data["pairs"][0]["url"]
        url += "?maker="+address
        return url
    except requests.exceptions.RequestException as e:
        return f"Erreur lors de la récupération du prix : {e}"
def get_aptos_price():
    address = "0x1::aptos_coin::AptosCoin"
    url = f"https://api.dexscreener.com/latest/dex/tokens/{address}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if 'pairs' in data:
            for pair in data['pairs']:
                if pair['baseToken']['address'] == address or pair['quoteToken']['address'] == address:
                    price = pair['priceUsd']
                    return float(price)

    except requests.exceptions.RequestException as e:
        return f"Erreur lors de la récupération du prix : {e}"