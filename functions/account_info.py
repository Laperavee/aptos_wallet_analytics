from aptoswallet.functions.token_info import *
from aptoswallet.comon.res import *

def get_transactions(address):
    url = URL + f'accounts/{address}/transactions'
    print(url)
    transactions = request(url)
    swap_events = []
    for transaction in transactions:
        events = transaction.get("events", [])
        for event in events:
            if "SwapEvent" in event.get('type', ''):
                event_type = event.get('type').split("<")[1].split(">")[0].split(",")[0]
                data = event.get('data', {})
                token = event_type.split("::")
                decimals = token_info_search(token[0])
                x_in = round(int(data.get('x_in', 0)) / (10 ** decimals),2)
                x_out = round(int(data.get('x_out', 0)) / (10 ** decimals),2)
                y_in = int(data.get('y_in', 0)) / 100000000
                y_out = int(data.get('y_out', 0)) / 100000000
                swap_events.append({
                    'address':event_type,
                    'token': token[1].split("::")[0],
                    'x_in': x_in,
                    'x_out': x_out,
                    'y_in': y_in,
                    'y_out': y_out
                })
    return swap_events

def sort_items(transactions):
    grouped_transactions = {}
    for transaction in transactions:
        address = transaction['address']
        token = transaction['token']
        x_in = transaction['x_in']
        x_out = transaction['x_out']
        y_in = transaction['y_in']
        y_out = transaction['y_out']
        if token not in grouped_transactions:
            grouped_transactions[token] = {
                'address': address,
                'token': token,
                'transactions': []
            }
        grouped_transactions[token]['transactions'].append({
            'x_in': x_in,
            'x_out': x_out,
            'y_in': y_in,
            'y_out': y_out
        })
    result = []
    for token, data in grouped_transactions.items():
        result.append({
            'address': data['address'],
            'token': data['token'],
            'transactions': data['transactions']
        })
    return result

def get_positions(transactions,address):
    positions = {}
    for transaction in transactions:
        token = transaction['token']
        token_address = transaction['address']
        if token not in positions:
            positions[token] = {'remaining': 0, 'y_in_total': 0, 'y_out_total': 0}
        for tx in transaction['transactions']:
            positions[token]['y_in_total'] += tx['y_in']
            positions[token]['y_out_total'] += tx['y_out']
        remaining_tokens = get_remaining_tokens(token_address, address)
        decimals = token_info_search(token_address.split("::")[0])
        positions[token]['remaining'] = remaining_tokens / (10**decimals)
        positions[token]['address'] = token_address
    return positions

def calculate_pnl(positions):
    pnl = {}
    winrate = 0
    total_pnl = 0
    sum_of = 0
    for token, data in positions.items():
        remaining = round(data["remaining"], 0)
        token_price = get_token_price(data["address"])
        if data["y_in_total"] != 0:
            pnl[token] = {}
            remaining_usd = remaining * token_price
            in_usd = data["y_in_total"] * get_aptos_price()
            out_usd = data["y_out_total"] * get_aptos_price()
            dollars = round((out_usd + remaining_usd - in_usd), 2)
            pnl[token]["remaining"] = round(remaining_usd,0)
            pnl[token]["percentage"] = round((((out_usd + remaining_usd) - in_usd) / in_usd) * 100, 2)
            pnl[token]["dollars"] = dollars
        else:
            continue
        if pnl[token]["percentage"] > 0:
            winrate += 1
        elif pnl[token]["percentage"] == 0:
            sum_of-=1
        total_pnl += pnl[token]["dollars"]
        sum_of += 1
    pnl["winrate"] = round((winrate / sum_of) * 100, 2)
    pnl["total_pnl"] = round(total_pnl, 0)
    return pnl

def calculate_open_position(positions):
    open_trades = {}
    for token, data in positions.items():
        remaining = abs(data['remaining'])
        price = get_token_price(data['address'])
        if price is not None:
            open_trades[token] = {
                'remaining': round(float(remaining) * float(price),2),
            }
        else:
            open_trades[token] = {
                'remaining': "Prix non trouvé.",
            }
    return open_trades
