from flask import Flask
from igdb.wrapper import IGDBWrapper
from helpers import igdb_authenticate

app = Flask(__name__)
app.config.from_prefixed_env()
CLIENT_ID = app.config["CLIENT_ID"]
CLIENT_SECRET = app.config["CLIENT_SECRET"]

ACCESS_TOKEN = igdb_authenticate(CLIENT_ID, CLIENT_SECRET)
wrapper = IGDBWrapper(CLIENT_ID, ACCESS_TOKEN)

@app.route('/')
def hello_world():
    byte_array = wrapper.api_request(
        endpoint='games',
        query='fields id, name; limit 10;'
    )
    print(byte_array)
    return byte_array
