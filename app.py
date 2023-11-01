from flask import Flask, render_template
from helpers import igdb_authenticate, igdb_query

app = Flask(__name__)
app.config.from_prefixed_env()
CLIENT_ID = app.config["CLIENT_ID"]
CLIENT_SECRET = app.config["CLIENT_SECRET"]
ACCESS_TOKEN = igdb_authenticate(CLIENT_ID, CLIENT_SECRET)

@app.route('/')
def index():
    games = igdb_query(CLIENT_ID, ACCESS_TOKEN, 'games', 'fields name, cover.image_id; where rating > 90; limit 6;')
    return render_template('index.html', games=games)
