import os

import discord
import re
from discord import Option
from handle_ratio import handle_ratio
import requests

ratio_counter_regex = r"(?:^|\W)ratio+(?:$|\W)|counter(?:$|\W)"

intents = discord.Intents.none()
intents.messages = True
intents.message_content = True
intents.guild_reactions = True
bot = discord.Bot(intents=intents)

allowed_guild_ids = []


@bot.event
async def on_ready():
    print(f'Logged on as {bot.user}')


@bot.event
async def on_message(message):
    # Don't let the bot reply to itself
    if message.author == bot.user:
        return

    content = message.content.lower()

    # Send link to source code
    if content == 'ratio bot send code!!':
        await message.channel.send('https://github.com/idkwuu/RatioTerminal', reference=message)

    # Check if message is a ratio or a counter
    message_is_ratio_or_counter = re.search(ratio_counter_regex, content) is not None
    if message_is_ratio_or_counter:
        await handle_ratio(message)


@bot.slash_command(guild_ids=[])
async def leaderboards(ctx):
    await ctx.respond("Work in progress.")


@bot.slash_command(guild_ids=allowed_guild_ids, description='Get your ✨ ratio score ✨')
async def score(ctx, user: Option(discord.Member, description="Expose someone's (or yours) ratio score")):
    if bot.user == user:
        await ctx.respond('My ✨ ratio score ✨ is ***infinite***. Btw, ratio declined.')
        return

    r = requests.get(f'{os.environ["RATIO_TERMINAL_LEADERBOARD_SERVER"]}/ratioterminal/score?user_id={user.id}')
    if r.status_code == 200:
        user_score = r.json()['score']
        await ctx.respond(f'Your ✨ ratio score ✨ is {user_score}')
    else:
        pass


bot.run(os.environ['RATIO_TERMINAL_TOKEN'])
