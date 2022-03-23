from flask import Flask, request
from db import *

app = Flask('RatioTerminalLeaderboard')


@app.route('/ratioterminal/score', methods=['POST', 'GET'])
def lb_set_score():
    user_id = request.args['user_id']
    if request.method == 'POST':
        score = lb_db_change_score(
            user_id,
            request.json['server_id'],
            request.json['score']
        )
    else:
        score = lb_db_get_user_score(user_id)
    return {
        'score': score
    }


lb_db_init()
app.run()
