import discord
import random
import datetime
from leaderboard import send_score_to_leaderboard

timeouts = {}


async def handle_ratio(message: discord.message):
    # Check if user is in 15 s timeout
    try:
        user_timeout = timeouts[message.author.id]
        seconds_since_timeout = (datetime.datetime.now() - user_timeout).total_seconds()
        if seconds_since_timeout < 15:
            await message.add_reaction('💀')
            return
    except KeyError:
        pass

    # Actually ratio or counter
    should_be_ratio = random.randint(0, 100) % 2 == 1
    send_score_to_leaderboard(message.author.id, message.guild.id, should_be_ratio)
    await message.add_reaction('👍' if should_be_ratio else '👎')
    await message.channel.send(
        'https://docs.idkwuu.dev/ratioaccepted.png' if should_be_ratio else 'https://docs.idkwuu.dev/ratiodeclined.png',
        reference=message)
    timeouts[message.author.id] = datetime.datetime.now()
