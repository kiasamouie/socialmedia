from instagram import InstagramAPI

# Replace with your actual app details
client_id = '1898887940636108'
client_secret = '6bbccdee2285379f7355e163f26ab1a5'
account_id = '17841468958222588'
auth_url = 'https://www.facebook.com/v18.0/dialog/oauth'
token_url = 'https://graph.facebook.com/v18.0/oauth/access_token'
redirect_uri = 'https://samui-music.com/redirect'

instagram_api = InstagramAPI(client_id, client_secret, account_id, auth_url, token_url, redirect_uri)

# Exchange short-lived token for long-lived token
short_lived_token = 'EAAaZCB00rfcwBO2sV7ZBaVPd1llw0SLowMh5ZCKLVT1yNCFGXgPHZAKOXSZB7P8VsXU8991sHMe1DgwoyaeyZA6ragdTtTb6UYKmiIKQCl9GPtGQBmMiSLgdwXwTrQGf3nH55QRseYhWJ9fjZCftPsZBsM75cfTkUeFMmo0cQqDAlaZAmDOFGDCykQTkflkrvjNtOBAZDZD'
long_lived_token = instagram_api.exchange_for_long_lived_token(short_lived_token)

print(long_lived_token)