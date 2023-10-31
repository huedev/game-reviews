import requests
import json

def igdb_authenticate(client_id, client_secret):
    """Authenticate as Twitch Developer to use IGDB"""
    url = (
        f"https://id.twitch.tv/oauth2/token"
        f"?client_id={client_id}"
        f"&client_secret={client_secret}"
        f"&grant_type=client_credentials"
    )

    try:
        response = requests.post(url)
        response.raise_for_status()
        data = json.loads(response.content)
        return data['access_token']
    except (requests.RequestException, ValueError, KeyError, IndexError) as e:
        print(e)
        return None