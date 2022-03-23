<img src="https://user-images.githubusercontent.com/42050584/140654544-6bc063e6-38ce-44d4-a151-be25f62eca1b.png" width=300 align="right">

# Ratio Terminal

Remember Twitter ratios? Well, here these are for discord.

There are currently 2 parts of this bot:

- `/discord_bot`: source code for the Discord bot
- `/leaderboard`: source code for the leaderboards. Optional.

### Discord bot

- Environment variables
  - `RATIO_TERMINAL_TOKEN`: the bot token
  - `RATIO_TERMINAL_LEADERBOARD_SERVER`: the address that hosts the server from `/leaderboard`.
    - For example:`http://localhost:8080`
- Required Python packages
  - requests
  - py-cord

### Leaderboard

- Required Python packages
  - Flask