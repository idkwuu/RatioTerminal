import re
from discord import Option
from handle_ratio import handle_ratio
from leaderboard import *

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
    await get_server_leaderboard(ctx, '392856522532585492')


@bot.slash_command(description='Get your ✨ ratio score ✨')
async def score(ctx,
                user: Option(discord.Member, description="Expose someone's (or yours) ratio score", required=False)):
    user_id = ctx.author.id if user is None else user.id

    if bot.user.id == user_id:
        await ctx.respond('My ✨ ratio score ✨ is ***infinite***. Btw, ratio declined.')
        return

    r = requests.get(f'{os.environ["RATIO_TERMINAL_LEADERBOARD_SERVER"]}/ratioterminal/score?user_id={user_id}')
    if r.status_code == 200:
        user_score = r.json()['score']
        if user is None:
            await ctx.respond(f'Your ✨ ratio score ✨ is {user_score}')
        else:
            await ctx.respond(f'{user}\'s ✨ ratio score ✨ is {user_score}')
    else:
        pass


bot.run(os.environ['RATIO_TERMINAL_TOKEN'])
