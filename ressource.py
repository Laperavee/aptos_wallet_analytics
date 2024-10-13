import requests

url = 'https://api.mainnet.aptoslabs.com/v1/accounts/0x2d4de7378c573dadc2e589892d709ee24f3c26f23b57804f384f4803da2e6f0a/resources'
response = requests.get(url)

if response.status_code == 200:
    resources = response.json()
    for resource in resources:
        event_type = resource.get("type", "")
        if "CoinInfo" in event_type:
            data = resource.get("data", {})
            decimals = data.get('decimals')
            print(f"decimals: {decimals}")
else:
    print(f"Échec de la récupération des ressources. Code d'état : {response.status_code}")
