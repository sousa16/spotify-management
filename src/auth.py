import os
import base64
import requests
import urllib.parse
import webbrowser


def get_authorization_url():
    """
    Build the Spotify authorization URL and open it in the user's browser.
    """
    client_id = os.environ.get("SPOTIFY_CLIENT_ID")
    redirect_uri = os.environ.get(
        "SPOTIFY_REDIRECT_URI", "http://127.0.0.1:8888/callback")
    scope = "user-library-read user-library-modify"
    auth_url = "https://accounts.spotify.com/authorize"
    params = {
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": redirect_uri,
        "scope": scope
    }
    url = f"{auth_url}?{urllib.parse.urlencode(params)}"
    print("Open this URL in your browser and authorize the app:")
    print(url)
    try:
        webbrowser.open(url)
    except Exception:
        pass
    return url


def exchange_code_for_token(code):
    """
    Exchange authorization code for access and refresh tokens.
    """
    client_id = os.environ.get("SPOTIFY_CLIENT_ID")
    client_secret = os.environ.get("SPOTIFY_CLIENT_SECRET")
    redirect_uri = os.environ.get(
        "SPOTIFY_REDIRECT_URI", "http://127.0.0.1:8888/callback")
    url = "https://accounts.spotify.com/api/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri,
        "client_id": client_id,
        "client_secret": client_secret
    }
    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()
    return response.json()


def refresh_access_token(refresh_token):
    """
    Refresh an access token using the Authorization Code flow.
    """
    client_id = os.environ.get("SPOTIFY_CLIENT_ID")
    client_secret = os.environ.get("SPOTIFY_CLIENT_SECRET")
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": "Basic " + base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    }
    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    }
    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()
    return response.json()
