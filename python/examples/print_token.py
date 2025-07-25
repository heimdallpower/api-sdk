import logging
from heimdall_api_client.auth import AuthService

logging.basicConfig(level=logging.WARN)

auth = AuthService(
    client_id="your_client_id",
    client_secret="your_client_secret",
    )

token = auth.get_valid_token()
print(f"Access Token: {token}")
print(f"Region: {auth.get_region_from_token()}")
print(f"Token Expiry: {auth.expires_at}")
