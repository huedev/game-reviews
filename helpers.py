import json

from flask import redirect, session
from requests import post, RequestException
from functools import wraps


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    # Referred to Problem Set 9 (CS50 Finance) for login_requried decorator logic
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def igdb_authenticate(client_id, client_secret):
    """Authenticate as Twitch Developer to use IGDB"""
    # Referred to Problem Set 9 (CS50 Finance) for building a response and querying API
    # Also referred to IGDB documentation (https://api-docs.igdb.com)
    url = (
        f'https://id.twitch.tv/oauth2/token'
        f'?client_id={client_id}'
        f'&client_secret={client_secret}'
        f'&grant_type=client_credentials'
    )

    try:
        response = post(url)
        response.raise_for_status()
        data = json.loads(response.content)
        return data['access_token']
    except (RequestException, ValueError, KeyError, IndexError):
        return None


def igdb_query(client_id, access_token, endpoint, query):
    """Send query to IGDB and retrieve result"""
    # Referred to IGDB documentation (https://api-docs.igdb.com) for building a response and querying API
    try:
        response = post(f'https://api.igdb.com/v4/{endpoint}', **{'headers': {'Client-ID': client_id, 'Authorization': f'Bearer {access_token}'},'data': query})
        return response.json()
    except (RequestException, ValueError, KeyError, IndexError):
        return None
