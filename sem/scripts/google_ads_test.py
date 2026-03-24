"""Quick test — verify Google Ads API connection."""

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
import yaml, os, warnings
warnings.filterwarnings("ignore")

CREDENTIALS_FILE = os.path.join(os.path.dirname(__file__), '..', 'config', 'credentials.yml')

with open(CREDENTIALS_FILE) as f:
    creds = yaml.safe_load(f)['google_ads']

config = {
    "developer_token": creds['developer_token'],
    "client_id": creds['client_id'],
    "client_secret": creds['client_secret'],
    "refresh_token": creds['refresh_token'],
    "use_proto_plus": True,
}

CUSTOMER_ID = str(creds['customer_id'])

try:
    client = GoogleAdsClient.load_from_dict(config)
    ga_service = client.get_service("GoogleAdsService")
    query = """
        SELECT customer.id, customer.descriptive_name, customer.currency_code,
               customer.time_zone, customer.status
        FROM customer LIMIT 1
    """
    response = ga_service.search(customer_id=CUSTOMER_ID, query=query)
    for row in response:
        c = row.customer
        print(f"Account:  {c.descriptive_name}")
        print(f"ID:       {c.id}")
        print(f"Currency: {c.currency_code}")
        print(f"Timezone: {c.time_zone}")
        print(f"Status:   {c.status.name}")
    print("\nGoogle Ads API fully operational.")
except GoogleAdsException as ex:
    for error in ex.failure.errors:
        print(f"Google Ads error: {error.message}")
except Exception as e:
    print(f"Error: {e}")
