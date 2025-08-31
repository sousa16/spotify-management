import requests
import os


def get_all_episode_ids(access_token):
    """
    Fetch all saved episode IDs for the user, handling pagination.
    Args:
        access_token (str): Valid Spotify access token.
    Returns:
        list: All episode IDs in user's library.
    """
    url = "https://api.spotify.com/v1/me/episodes"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    episode_ids = []
    params = {"limit": 50, "offset": 0}
    while True:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        items = data.get('items', [])
        episode_ids.extend([ep['episode']['id'] for ep in items])
        if not data.get('next'):
            break
        params['offset'] += params['limit']
    return episode_ids


def remove_episodes(access_token, episode_ids):
    """
    Remove one or more episodes from the user's library.
    Args:
        access_token (str): Valid Spotify access token.
        episode_ids (list): List of episode IDs to remove.
    Returns:
        bool: True if successful, False otherwise.
    """
    url = "https://api.spotify.com/v1/me/episodes"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    params = {
        "ids": ','.join(episode_ids)
    }
    response = requests.delete(url, headers=headers, params=params)
    if response.status_code == 200 or response.status_code == 204:
        return True
    else:
        print(f"Failed to remove episodes: {response.text}")
        return False


"""
Episode management functions for Spotify Management CLI tool.
Provides utilities to interact with user's saved episodes.
"""


def get_my_episodes(access_token):
    """
    Get the current user's saved episodes from Spotify.
    Args:
        access_token (str): Valid Spotify access token.
    Returns:
        dict: JSON response containing user's saved episodes.
    """
    url = "https://api.spotify.com/v1/me/episodes"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()
