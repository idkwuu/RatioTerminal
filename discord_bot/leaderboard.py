import json

import discord.ext.commands
import requests
import os


def send_score_to_leaderboard(user_id: str, server_id: str, was_accepted: bool):
    r = requests.post(
        url=f'{os.environ["RATIO_TERMINAL_LEADERBOARD_SERVER"]}/ratioterminal/score?user_id={user_id}',
        headers={'Content-Type': 'application/json'},
        data=json.dumps({
            'score': 1 if was_accepted else -1,
            'server_id': server_id
        })
    )


async def get_server_leaderboard(ctx: discord.ApplicationContext, server_id: str):
    r = requests.get(
        f'{os.environ["RATIO_TERMINAL_LEADERBOARD_SERVER"]}/ratioterminal/leaderboard?server_id={server_id}')
    scores = r.json()
    description = []
    for s in scores:
        description.append(f'<@{s["user_id"]}> - `{s["score"]}`')
    embed = discord.Embed(
        title='✨ Ratio Leaderboard',
        description='\n'.join(description)
    )
    await ctx.respond(embed=embed)
