# Import required Python modules
import geopandas as gpd
import requests
from getpass import getpass
import matplotlib.pyplot as plt

# Request ACLED credentials at runtime
acled_email = input("ACLED email: ")
acled_password = getpass("ACLED password: ")

# Define the ACLED OAuth token endpoint
token_url = "https://acleddata.com/oauth/token"

# Define the information required to request an ACLED access token
token_data = {
    'username': acled_email,
    'password': acled_password,
    'grant_type': 'password',
    'client_id': 'acled',
    'scope': 'authenticated'
}

# Send the authentication request to ACLED
token_response = requests.post(token_url, data=token_data, timeout=30)

print(f"Authentication status: {token_response.status_code}")

# Extract the access token from the authentication response
response_data = token_response.json()
acled_token = response_data["access_token"]

# Create the authentication header for ACLED API requests
headers = {
    "Authorization": f"Bearer {acled_token}"
}

# Define the ACLED event data endpoint
acled_url = "https://acleddata.com/api/acled/read"

# Define filters for the Ukraine conflict event request
params = {
    "country": "Ukraine",
    "event_date": "2025-07-01|2025-07-31",
    "event_date_where": "BETWEEN",
    "limit": 5
}

# Request filtered conflict event data from ACLED
response = requests.get(
    acled_url,
    headers=headers,
    params=params,
    timeout=30
)
print(f"Event request status: {response.status_code}")

# Extract the returned ACLED conflict event records
api_data = response.json()
records = api_data["data"]
print(len(records))

# Load Ukraine ADM1 administrative boundaries
oblasts = gpd.read_file('data/boundaries/geoBoundaries-UKR-ADM1-all/geoBoundaries-UKR-ADM1.geojson')
print(oblasts.head())
print(oblasts.columns)
print(oblasts.crs)
print(f"Number of administrative regions: {len(oblasts)}")
print(oblasts['shapeName'].tolist())
oblasts.plot()
plt.show()