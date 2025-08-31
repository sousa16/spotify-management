"""
Local Flask server to automatically capture Spotify authorization code from browser redirect.
Used in the authentication flow for the CLI tool.
"""
from flask import Flask, request
import threading

app = Flask(__name__)
code_holder = {}


@app.route('/callback')
def callback():
    """
    Flask route handler for /callback.
    Captures the authorization code from the redirect and stores it.
    """
    code = request.args.get('code')
    code_holder['code'] = code
    return f"Authorization code received! You can close this tab.\n"


def run_server():
    """
    Start the Flask server on port 8888.
    """
    app.run(port=8888)


def get_code_from_browser():
    """
    Start the local server and wait for the authorization code from browser redirect.
    Returns:
        str: The authorization code received from Spotify.
    """
    # Start Flask server in a separate thread
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()
    print("Waiting for authorization code...")
    while 'code' not in code_holder:
        pass
    return code_holder['code']
