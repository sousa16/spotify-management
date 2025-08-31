

"""
Main entry point for Spotify Management CLI tool.
Handles user authentication, token exchange, and episode management.
"""

import os
import json
from dotenv import load_dotenv
from auth import get_authorization_url, exchange_code_for_token, refresh_access_token
from episodes import get_my_episodes, remove_episodes
from capture_code import get_code_from_browser
import requests


def main():
    """
    Authenticate user, obtain tokens, and let user choose to list or delete episodes.
    Automatically refresh access token if expired.
    """
    load_dotenv()  # Load environment variables from .env file

    # Try to load refresh token from file
    token_path = os.path.expanduser("~/.spotify_refresh_token.json")
    refresh_token = None
    access_token = None
    if os.path.exists(token_path):
        with open(token_path, "r") as f:
            data = json.load(f)
            refresh_token = data.get("refresh_token")

    if refresh_token:
        print("Using saved refresh token.")
        tokens = refresh_access_token(refresh_token)
        access_token = tokens["access_token"]
        # Save new refresh token if provided
        if "refresh_token" in tokens:
            refresh_token = tokens["refresh_token"]
            with open(token_path, "w") as f:
                json.dump({"refresh_token": refresh_token}, f)
        print("Access token refreshed.")
    else:
        # Step 1: Guide user to authorize and get code
        print("Step 1: Authorize the app")
        get_authorization_url()
        code = get_code_from_browser()  # Automatically capture code from browser redirect

        # Step 2: Exchange code for tokens
        tokens = exchange_code_for_token(code)
        access_token = tokens["access_token"]
        refresh_token = tokens.get("refresh_token")
        print("Access token:", access_token)
        print("Refresh token:", refresh_token)
        # Save refresh token for future use
        if refresh_token:
            with open(token_path, "w") as f:
                json.dump({"refresh_token": refresh_token}, f)

    # Step 3: Prompt user for action
    print("\nWhat would you like to do?")
    print("1. List all episodes (prettified)")
    print("2. Delete all episodes from 'My Episodes'")
    choice = input("Enter 1 or 2: ").strip()

    # Step 4: Use access token for API requests
    try:
        episodes_data = get_my_episodes(access_token)
    except requests.exceptions.HTTPError as e:
        # If token expired, refresh and retry
        if e.response.status_code == 401 and refresh_token:
            print("Access token expired. Refreshing...")
            tokens = refresh_access_token(refresh_token)
            access_token = tokens["access_token"]
            print("New access token acquired")
            episodes_data = get_my_episodes(access_token)
        else:
            raise

    episodes = episodes_data.get('items', [])

    if choice == "1":
        print("\nYour Saved Episodes:")
        # Paginate through all episodes
        url = "https://api.spotify.com/v1/me/episodes"
        headers = {"Authorization": f"Bearer {access_token}"}
        params = {"limit": 50, "offset": 0}
        total_count = 0
        while True:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            items = data.get('items', [])
            for ep in items:
                show = ep['episode']['show']['name']
                name = ep['episode']['name']
                release = ep['episode']['release_date']
                print(f"- {name} ({show}) - Released: {release}")
                total_count += 1
            if not data.get('next'):
                break
            params['offset'] += params['limit']
        print(f"\nTotal episodes listed: {total_count}")
    elif choice == "2":
        from episodes import get_all_episode_ids
        all_episode_ids = get_all_episode_ids(access_token)
        if not all_episode_ids:
            print("No episodes to delete.")
        else:
            print(f"Deleting {len(all_episode_ids)} episodes...")
            # Batch delete, max 50 per request
            for i in range(0, len(all_episode_ids), 50):
                batch = all_episode_ids[i:i+50]
                success = remove_episodes(access_token, batch)
                if not success:
                    print(f"Failed to delete batch {i//50+1}.")
            print("All episodes deleted from 'My Episodes'.")
    else:
        print("Invalid choice.")


if __name__ == "__main__":
    main()
