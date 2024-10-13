from functions.account_info import *
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.command()
async def scan(ctx, address: str):
    print(address)
    pnl = calculate_pnl(get_positions(sort_items(get_transactions(address)), address))

    if pnl is None:
        await ctx.reply("Erreur lors de la récupération des données.")
        return
    if not pnl:
        await ctx.reply("Aucune position ouverte trouvée.")
        return

    embed = discord.Embed(title="📊 PnL", color=discord.Color.green())

    for token, data in pnl.items():
        print(data)
        if token in ["winrate", "total_pnl"]:
            continue
        if data['dollars'] >= 0:
            pnl_text = f"{data['dollars']}"
            colored_pnl = f"```diff\n+ {pnl_text} $```"
        else:
            pnl_text = f"{abs(data['dollars'])}"
            colored_pnl = f"```diff\n- {pnl_text} $```"

        if data['percentage'] >= 0:
            percentage_text = f"{data['percentage']}"
            colored_percentage = f"```diff\n+ {percentage_text} %```"
        else:
            percentage_text = f"{abs(data['percentage'])}"
            colored_percentage = f"```diff\n- {percentage_text} %```"

        embed.add_field(
            name=f"📈 **{token}** ",
            value=(f"💰 **Remaining : {data['remaining']} $**\n"
                   f"{colored_percentage}"
                   f"{colored_pnl}\n"),
            inline=False
        )
    embed.add_field(name="📈 **Winrate : **", value=f"{pnl['winrate']} %", inline=False)
    embed.add_field(name="📈 **Total PnL : **", value=f"{pnl['total_pnl']} $", inline=False)

    await ctx.reply(embed=embed)

@bot.command()
async def aptos(ctx):
    aptos_emoji = '<:aptos:1295025396152274956>'
    price = get_aptos_price()
    embed = discord.Embed(title=f"{aptos_emoji} ** APT = {price} $**", color=discord.Color.blue())
    await ctx.reply(embed=embed)

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
