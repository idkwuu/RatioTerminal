import json
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
