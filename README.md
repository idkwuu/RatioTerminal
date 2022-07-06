<p align="center">
  <img src="https://i.imgur.com/DVlmu6m.png" width="300"/>
</p>

<h1 align="center">Ratio Terminal</h1>
<p align="center">Remember Twitter ratios? Well, here these are for Discord.</p>

<a href="https://hub.docker.com/r/idkwuu/ratioterminal"><p align="center">Docker Hub</p></a>

### Running

Tested with Python 3.10

- `pip install -r requirements.txt`
- `python3 src/main.py`

### Docker

**Environment variables**

| Variable | Description |
| ----------- | ----------- |
| RATIO_TERMINAL_TOKEN | Discord bot token|

**Optional mounts**

| Folder | Description |
| ----------- | ----------- |
| /data |Contains leaderboard database |

### License

MIT