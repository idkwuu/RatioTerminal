import re
import discord

from handle_ratio import handle_ratio
import leaderboard as lb
import os
from database import db_init

import asyncio

ratio_counter_regex = r"(?:^|\W)ratio+(?:$|\W)|counter(?:$|\W)"

intents = discord.Intents.none()
intents.messages = True
intents.message_content = True
intents.guild_reactions = True
bot = discord.Bot(intents=intents)


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
        return

    # Check if message is a ratio or a counter
    message_is_ratio_or_counter = re.search(ratio_counter_regex, content) is not None
    if message_is_ratio_or_counter:
        await handle_ratio(message)


@bot.slash_command(description='Get the server leaderboard')
async def leaderboard(ctx: discord.ApplicationContext):
    await lb.get_server_leaderboard(ctx)


@bot.slash_command(description='Get your ✨ ratio score ✨')
async def score(ctx: discord.ApplicationContext,
                user: discord.Option(discord.Member, description="Expose someone's (or yours) ratio score", required=False)):
    user_data = ctx.author if user is None else user
    user_id = user_data.id

    if bot.user.id == user_id:
        await ctx.respond('My ✨ ratio score ✨ is ***infinite***. Btw, ratio declined.')
        return

    data = await lb.get_user_score(ctx)
    global_score = data['global']
    server_score = data['server']
    await ctx.respond(embed=discord.Embed(
        title=f'✨ Ratio score - {user_data}',
        description=f'🌍 Global: {global_score}\n📍 This server: {server_score}'
    ))


if __name__ == '__main__':
    exist = os.path.isdir('data')
    if not exist:
        os.mkdir('data')
    db_init()
    asyncio.run(bot.run(os.environ['RATIO_TERMINAL_TOKEN']))