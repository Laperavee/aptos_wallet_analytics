import asyncio
import discord
from aptoswallet.functions.bdd import *
from aptoswallet.functions.token_info import *

def get_transactions_dexscreener(wallet_address):
    url = f"https://fullnode.mainnet.aptoslabs.com/v1/accounts/{wallet_address}/transactions"
    response = requests.get(url)
    return response.json()

async def monitor_wallet(ctx):
    print("Monitoring started!")
    last_checked_txns = {}

    while True:
        wallets = get_wallets()
        if not wallets:
            await ctx.send("Aucune adresse surveillée.")
            break
        for wallet_data in wallets:
            wallet_address = wallet_data['address']
            user_id = wallet_data['user_id']
            transactions = get_transactions_dexscreener(wallet_address)
            if transactions:
                latest_txn = transactions[-1]
                print(latest_txn["hash"])
                if wallet_address not in last_checked_txns:
                    last_checked_txns[wallet_address] = latest_txn['hash']
                elif latest_txn['hash'] != last_checked_txns[wallet_address]:
                    last_checked_txns[wallet_address] = latest_txn['hash']
                    if latest_txn['type'] == "user_transaction":
                        for event in latest_txn.get('events', []):
                            if "SwapEvent" in event.get('type', ''):
                                event_type = event.get('type', '')
                                decimals = token_info_search(event_type.split("<")[1].split("::")[0])
                                token_name = event_type.split(",")[0].split("::")[-1]
                                token_address = event_type.split("<")[1].split(",")[0]
                                print(token_address, wallet_address)
                                url = get_token_info(token_address, wallet_address)

                                x_in = int(event['data']['x_in'])
                                x_out = int(event['data']['x_out'])
                                y_in = int(event['data']['y_in'])
                                y_out = int(event['data']['y_out'])

                                embed = discord.Embed(title=f"📈 **Swap detected**", color=discord.Color.green())
                                dexscreener_emoji = '<:dexscreener:1295025396152274956>'

                                if x_in != 0:
                                    await ctx.send(f"<@{user_id}>")
                                    embed.add_field(
                                        name="",
                                        value=(f"[{dexscreener_emoji} chart]({url})\n"
                                               f"```diff\n- SELL ```\n"
                                               f" **{round(x_in / (10 ** decimals), 2)}** {token_name} for **{round(y_out / (10 ** 8), 2)}** APT"),
                                        inline=False
                                    )
                                    await ctx.send(embed=embed)

                                elif x_out != 0:
                                    await ctx.send(f"<@{user_id}>")
                                    embed.add_field(
                                        name=f"",
                                        value=(f"[{dexscreener_emoji} chart]({url})\n"
                                               f"```diff\n+ BUY ```\n"
                                               f" **{round(x_out / (10 ** decimals), 2)}** {token_name} for **{round(y_in / (10 ** 8), 2)}** APT"),
                                        inline=False
                                    )
                                    await ctx.send(embed=embed)
        await asyncio.sleep(10)