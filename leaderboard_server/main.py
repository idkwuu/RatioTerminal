import json

import flask
from flask import Flask, request
from db import *

app = Flask('RatioTerminalLeaderboard')


@app.route('/ratioterminal/score', methods=['POST', 'GET'])
def lb_score():
    user_id = request.args['user_id']
    server_id = request.args['server_id']
    if request.method == 'POST':
        score = lb_db_change_score(
            user_id,
            server_id,
            request.json['score']
        )
        res = flask.Response(json.dumps({'score': score}))
    else:
        global_score = lb_db_get_user_score(user_id)
        server_score = lb_db_get_user_server_score(user_id, server_id)
        res = flask.Response(json.dumps({'global': global_score, 'server': server_score}))
    res.headers['Content-Type'] = 'application/json'
    return res


@app.route('/ratioterminal/leaderboard', methods=['GET'])
def lb_get_server():
    scores = lb_db_get_server_leaderboard(request.args['server_id'])
    leaderboard = []
    for s in scores:
        leaderboard.append({'user_id': s[0], 'score': s[1]})
    res = flask.Response(json.dumps(leaderboard))
    res.headers['Content-Type'] = 'application/json'
    return res


lb_db_init()
app.run()
