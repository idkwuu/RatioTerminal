import discord.ext.commands
import database


def send_score_to_leaderboard(user_id: str, server_id: str, was_accepted: bool):
    database.change_score(
        user_id,
        server_id,
        1 if was_accepted else -1
    )


async def get_server_leaderboard(ctx: discord.ApplicationContext):
    scores = database.get_server_leaderboard(str(ctx.guild.id))
    embed_description = []
    for s in scores:
        embed_description.append(f'<@{s[0]}> - `{s[1]}`')
    embed = discord.Embed(
        title='✨ Ratio Leaderboard',
        description='\n'.join(embed_description)
    )
    await ctx.respond(embed=embed)


async def get_user_score(ctx: discord.ApplicationContext):
    global_score = database.get_user_score(str(ctx.user.id))
    server_score = database.get_user_server_score(str(ctx.user.id), str(ctx.guild.id))
    return {
        'global': global_score,
        'server': server_score
    }
