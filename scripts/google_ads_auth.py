"""
Google Ads OAuth2 — get refresh token
Runs a local server, opens your browser automatically, exchanges the code.
Credentials are loaded from config/credentials.yml
"""

from google_auth_oauthlib.flow import InstalledAppFlow
import yaml, os

CREDENTIALS_FILE = os.path.join(os.path.dirname(__file__), '..', 'config', 'credentials.yml')

with open(CREDENTIALS_FILE) as f:
    creds = yaml.safe_load(f)['google_ads']

SCOPES = ["https://www.googleapis.com/auth/adwords"]

client_config = {
    "installed": {
        "client_id": creds['client_id'],
        "client_secret": creds['client_secret'],
        "redirect_uris": ["http://localhost"],
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
    }
}

print("\nOpening browser for Google authentication...")
flow = InstalledAppFlow.from_client_config(client_config, scopes=SCOPES)
credentials = flow.run_local_server(port=9090, prompt="consent", access_type="offline", open_browser=True)

refresh_token = credentials.refresh_token
print(f"\nRefresh token obtained and saved to config/credentials.yml")

with open(CREDENTIALS_FILE) as f:
    content = f.read()

content = content.replace(
    "  refresh_token:   # filled after OAuth flow",
    f"  refresh_token: {refresh_token}"
)

with open(CREDENTIALS_FILE, 'w') as f:
    f.write(content)

print("Done! Google Ads API is ready.")
