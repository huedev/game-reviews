import json

from requests import post, RequestException

def igdb_authenticate(client_id, client_secret):
    """Authenticate as Twitch Developer to use IGDB"""
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
    try:
        response = post(f'https://api.igdb.com/v4/{endpoint}', **{'headers': {'Client-ID': client_id, 'Authorization': f'Bearer {access_token}'},'data': query})
        return response.json()
    except (RequestException, ValueError, KeyError, IndexError):
        return None
