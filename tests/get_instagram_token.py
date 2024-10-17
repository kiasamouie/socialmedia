import os
import sys
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from socials.instagram import InstagramAPI
load_dotenv()

# Get credentials from environment variables
client_id = os.getenv('INSTAGRAM_CLIENT_ID')
client_secret = os.getenv('INSTAGRAM_CLIENT_SECRET')
account_id = os.getenv('INSTAGRAM_ACCOUNT_ID')
auth_url = os.getenv('INSTAGRAM_AUTH_URL')
token_url = os.getenv('INSTAGRAM_TOKEN_URL')
redirect_uri = os.getenv('INSTAGRAM_REDIRECT_URI')
short_lived_token = os.getenv('INSTAGRAM_SHORT_LIVED_TOKEN')

# Create Instagram API instance
instagram_api = InstagramAPI(client_id, client_secret, account_id, auth_url, token_url, redirect_uri)

# Exchange short-lived token for long-lived token
long_lived_token = instagram_api.exchange_for_long_lived_token(short_lived_token)

print(long_lived_token)
