# Import required Python modules
import geopandas as gpd
import pandas as pd
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
    "event_date": "2025-07-12|2025-07-18",
    "event_date_where": "BETWEEN",
    "limit": 5000,
    "with_total": "true"
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
print(f"Total events for study week: {api_data['total_count']}")
records = api_data["data"]
print(len(records))

# Convert the ACLED event records into a Pandas DataFrame
events_df = pd.DataFrame(records)

# Inspect the available ACLED event attributes
print(events_df.columns)

# Inspect key attributes required for the spatial analysis
print(events_df[["event_date", "event_type", "sub_event_type", "admin1", "latitude", "longitude"]].head())

# Check data types before spatial processing
print(events_df[["event_date", "latitude", "longitude"]].dtypes)

# Convert event dates to a datetime data type
events_df["event_date"] = pd.to_datetime(events_df["event_date"])
print(events_df["event_date"].dtype)

# Convert coordinates to numeric values
events_df["latitude"] = pd.to_numeric(
    events_df["latitude"],
    errors="coerce"
)
events_df["longitude"] = pd.to_numeric(
    events_df["longitude"],
    errors="coerce"
)
print(events_df[["latitude", "longitude"]].dtypes)

# Check for missing coordinate values
print(events_df[["latitude", "longitude"]].isna().sum())

# Convert ACLED coordinates into spatial point features
geometry = gpd.points_from_xy(
    events_df["longitude"],
    events_df["latitude"]
)

events_gdf = gpd.GeoDataFrame(
    events_df,
    geometry=geometry,
    crs="EPSG:4326"
)

# Check the event GeoDataFrame
print(events_gdf.crs)
print(events_gdf[["longitude", "latitude", "geometry"]].head())

# Select ACLED attributes required for the analysis
analysis_gdf = events_gdf[[
    "event_id_cnty",
    "event_date",
    "event_type",
    "sub_event_type",
    "admin1",
    "location",
    "latitude",
    "longitude",
    "fatalities",
    "geometry"
]].copy()
print(analysis_gdf.crs)
print(analysis_gdf.shape)

# Load Ukraine ADM1 administrative boundaries
oblasts = gpd.read_file('data/boundaries/geoBoundaries-UKR-ADM1-all/geoBoundaries-UKR-ADM1.geojson')
print(oblasts.head())
print(oblasts.columns)
print(oblasts.crs)
print(f"Number of administrative regions: {len(oblasts)}")
print(oblasts['shapeName'].tolist())

# Plot ACLED event points over Ukraine administrative boundaries
ax = oblasts.plot(facecolor="none", edgecolor="black")
events_gdf.plot(ax=ax, color="red", markersize=30)
plt.show()
