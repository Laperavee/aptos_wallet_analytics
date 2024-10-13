from functions.account_info import *
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.command()
async def scan(ctx, address: str):
    print(address)
    positions = get_positions(sort_items(get_transactions(address)),address)

    if positions is None:
        await ctx.reply("Erreur lors de la récupération des données.")
        return

    if not positions:
        await ctx.reply("Aucune position ouverte trouvée.")
        return

    response_message = ">>> PnL :\n"
    for token, data in positions.items():
        response_message += (
            f"📈 **Token :** {token}\n"
            f"💰 **Reste :** {data['remaining']}\n"
            f"📊 **Total Y In :** {data['y_in_total']}\n"
            f"📉 **Total Y Out :** {data['y_out_total']}\n"
            f"---\n"
        )
    await ctx.reply(response_message)

@bot.command()
async def positions(ctx, address: str):
    positions = calculate_open_position(get_positions(sort_items(get_transactions(address)),address))
    if positions is None:
        await ctx.reply("Erreur lors de la récupération des données.")
        return

    if not positions:
        await ctx.reply("Aucune position ouverte trouvée.")
        return

    sorted_positions = sorted(positions.items(), key=lambda item: item[1]['remaining'], reverse=True)
    embed = discord.Embed(title=f"🔍 **Open positions **", color=discord.Color.blue())
    for token, data in sorted_positions:
        embed.add_field(name=f"📈 Token : {token}", value=f"💰 Unrealized : **{data['remaining']} $**", inline=False)
    await ctx.reply(embed=embed)

token = "YOUR_API_TOKEN"
bot.run(token)
