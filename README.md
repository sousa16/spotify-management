# Spotify Management  

Take back control of your Spotify library.  

⚠️ **Disclaimer**: This project is not affiliated with or endorsed by Spotify. Use responsibly.  

---

## ✨ Features  

- **Clear episodes from “My Episodes” in one go**  
- Designed to be **extensible**

---


## 🚀 Getting Started

### Prerequisites
- Spotify account
- Spotify Developer App (Client ID & Client Secret)

### Installation
```bash
git clone git@github.com:sousa16/spotify-management.git
cd spotify-management
pip install -r requirements.txt
```

### Setup
1. Create a `.env` file in the project root with:
	```env
	SPOTIFY_CLIENT_ID=your-client-id
	SPOTIFY_CLIENT_SECRET=your-client-secret
	SPOTIFY_REDIRECT_URI=http://127.0.0.1:8888/callback
	```
2. Run the tool:
	```bash
	python src/main.py
	```
3. On first run, a browser window will open for Spotify authentication. After authorization, your refresh token will be saved to `~/.spotify_refresh_token.json` for future use. Subsequent runs will not require browser authentication unless the token is invalid or revoked.

### Usage
- **List all episodes**: Choose option 1 to see all your saved episodes, paginated and prettified.
- **Delete all episodes**: Choose option 2 to remove all episodes from "My Episodes" in batches (up to 50 per request).

### Security
- Do **not** commit your `.env` file or `~/.spotify_refresh_token.json` to version control.
- Your credentials and tokens are stored locally and are not shared.