"""
YouTube OAuth 2.0 authentication helper with persistent token storage.
Handles initial authorization flow and automatic token refresh.
"""

import os
import json
from pathlib import Path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# OAuth scopes for YouTube upload
SCOPES = [
    'https://www.googleapis.com/auth/youtube.upload',
    'https://www.googleapis.com/auth/youtube'
]

# Default file paths
DEFAULT_CLIENT_SECRETS = 'client_secrets.json'
DEFAULT_TOKEN_FILE = '.youtube_token.json'


def get_credentials(
    secrets_file: str = DEFAULT_CLIENT_SECRETS,
    token_file: str = DEFAULT_TOKEN_FILE,
    scopes: list[str] = SCOPES
) -> Credentials:
    """
    Load cached credentials or run OAuth flow.

    Flow:
    1. Check if token_file exists with valid credentials
    2. If expired but has refresh_token, refresh automatically
    3. If no valid credentials, launch browser-based OAuth flow
    4. Save credentials to token_file for future runs

    Args:
        secrets_file: Path to OAuth client secrets (from Google Cloud Console)
        token_file: Path to store/load cached credentials
        scopes: OAuth scopes to request

    Returns:
        Authenticated Credentials object

    Raises:
        FileNotFoundError: If secrets_file doesn't exist
        ValueError: If OAuth flow fails
    """
    credentials = None
    token_path = Path(token_file)
    secrets_path = Path(secrets_file)

    # Check for client secrets
    if not secrets_path.exists():
        print("\n" + "=" * 60)
        print("SETUP REQUIRED: YouTube API credentials not found")
        print("=" * 60)
        print(f"\nExpected file: {secrets_file}")
        print("\nTo set up YouTube API access:")
        print("1. Go to https://console.cloud.google.com")
        print("2. Create a new project (or select existing)")
        print("3. Enable 'YouTube Data API v3':")
        print("   - APIs & Services > Library > search 'YouTube Data API v3'")
        print("4. Create OAuth credentials:")
        print("   - APIs & Services > Credentials > Create Credentials")
        print("   - Select 'OAuth client ID' > 'Desktop app'")
        print("5. Download the JSON file")
        print(f"6. Save it as '{secrets_file}' in the project root")
        print("\n" + "=" * 60)
        raise FileNotFoundError(f"OAuth credentials file not found: {secrets_file}")

    # Try to load existing token
    if token_path.exists():
        try:
            credentials = Credentials.from_authorized_user_file(str(token_path), scopes)
        except Exception as e:
            print(f"Warning: Could not load cached credentials: {e}")
            credentials = None

    # Check if credentials need refresh or are missing
    if credentials and credentials.expired and credentials.refresh_token:
        print("Refreshing expired access token...")
        try:
            credentials.refresh(Request())
            _save_credentials(credentials, token_path)
            print("Token refreshed successfully.")
        except Exception as e:
            print(f"Warning: Token refresh failed: {e}")
            credentials = None

    # Run OAuth flow if no valid credentials
    if not credentials or not credentials.valid:
        print("\nStarting OAuth authorization flow...")
        print("A browser window will open for you to authorize access.")
        print("(If it doesn't open, check your terminal for the URL)\n")

        flow = InstalledAppFlow.from_client_secrets_file(str(secrets_path), scopes)
        credentials = flow.run_local_server(
            port=8080,
            success_message="Authorization successful! You can close this tab."
        )

        _save_credentials(credentials, token_path)
        print(f"\nCredentials saved to {token_file}")
        print("Future uploads will not require re-authorization.\n")

    return credentials


def _save_credentials(credentials: Credentials, token_path: Path) -> None:
    """Save credentials to JSON file."""
    token_data = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }
    with open(token_path, 'w') as f:
        json.dump(token_data, f, indent=2)


def build_youtube_client(credentials: Credentials = None):
    """
    Build YouTube Data API v3 client.

    Args:
        credentials: OAuth credentials (if None, will attempt to load/create)

    Returns:
        YouTube API client resource
    """
    if credentials is None:
        credentials = get_credentials()

    return build('youtube', 'v3', credentials=credentials)


def verify_authentication() -> bool:
    """
    Verify that authentication is working by making a simple API call.

    Returns:
        True if authentication is valid, False otherwise
    """
    try:
        youtube = build_youtube_client()
        # Simple API call to verify credentials
        youtube.channels().list(part='id', mine=True).execute()
        return True
    except Exception as e:
        print(f"Authentication verification failed: {e}")
        return False


if __name__ == '__main__':
    # Test authentication when run directly
    print("Testing YouTube API authentication...")
    if verify_authentication():
        print("Authentication successful!")
    else:
        print("Authentication failed. Please check your credentials.")
