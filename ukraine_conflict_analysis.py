# Import required Python modules
import geopandas as gpd
import pandas as pd
import requests
from getpass import getpass
import matplotlib.pyplot as plt

def load_boundaries(file_path):
    """
    Load the oblast boundaries dataset.

    Parameters
    ----------
    file_path : str
        Path to the oblast boundary dataset.

    Returns
    -------
    GeoDataFrame
        Loaded spatial dataset.
    """

    data = gpd.read_file(file_path)

    return data

def calculate_oblast_areas(boundaries):
    """
    Calculate the area of each oblast in square kilometres.

    Parameters
    ----------
    boundaries : GeoDataFrame
        Oblast boundary data.

    Returns
    -------
    GeoDataFrame
        Oblast boundary data containing area values.
    """

    # Reproject boundaries for area calculation
    oblasts_area = boundaries.to_crs(epsg=10596)

    # Calculate area in square kilometres
    oblasts_area["area_km2"] = oblasts_area.geometry.area / 1_000_000

    return oblasts_area

def prepare_event_data(records):
    """
    Prepare ACLED event records for spatial analysis.

    Parameters
    ----------
    records : list
        ACLED event records returned by the API.

    Returns
    -------
    GeoDataFrame
        Prepared conflict event data with point geometry.
    """

    # Convert ACLED records to a Pandas DataFrame
    events_df = pd.DataFrame(records)

    # Convert event dates to datetime values
    events_df["event_date"] = pd.to_datetime(events_df["event_date"])
    print(events_df["event_date"].dtype)

    # Convert coordinate fields to numeric values
    events_df["latitude"] = pd.to_numeric(
        events_df["latitude"],
        errors="coerce"
    )
    events_df["longitude"] = pd.to_numeric(
        events_df["longitude"],
        errors="coerce"
    )

    # Check for missing coordinate values
    print(events_df[["latitude", "longitude"]].isna().sum())

    # Create point geometry from long and lat
    geometry = gpd.points_from_xy(
        events_df["longitude"],
        events_df["latitude"]
    )

    # Create a spatial GeoDataFrame using WGS 84
    events_gdf = gpd.GeoDataFrame(
        events_df,
        geometry=geometry,
        crs="EPSG:4326"
    )

    # Select attributes required for the analysis
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

    return analysis_gdf

def assign_events_to_oblasts(events, boundaries):
    """
    Assign conflict event points to oblast areas.

    Parameters
    ----------
    events : GeoDataFrame
        Conflict event point data.
    boundaries : GeoDataFrame
        Oblast boundary data.

    Returns
    -------
    GeoDataFrame
        Conflict events containing the assigned oblast area.
    """

    # Assign event points to oblast areas
    events_joined = gpd.sjoin(
        events,
        boundaries[["shapeName", "geometry"]],
        how="left",
        predicate="within"
    )

    return events_joined

def calculate_event_density(events_joined, oblast_areas):
    """
    Calculate conflict event counts and density by oblast area.

    Parameters
    ----------
    events_joined : GeoDataFrame
        Conflict events assigned to oblast areas.
    oblast_areas : GeoDataFrame
        Oblast boundary data containing area values.

    Returns
    -------
    GeoDataFrame
        Oblast areas containing event counts and event density.
    """

    # Count ACLED events by oblast area
    counts = events_joined.groupby("shapeName").size()

    # Convert event counts into a DataFrame
    event_counts = counts.to_frame(name="event_count").reset_index()

    # Combine oblast areas with event counts
    oblast_summary = oblast_areas.merge(
        event_counts,
        on="shapeName",
        how="left"
    )

    # Replace missing event counts with zero
    oblast_summary["event_count"] = oblast_summary["event_count"].fillna(0).astype(int)

    # Calculate events per 1,000 square kilometres
    oblast_summary["events_per_1000km2"] = (oblast_summary["event_count"] / oblast_summary["area_km2"]) * 1000

    return oblast_summary

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

# Prepare ACLED event records for spatial analysis
analysis_gdf = prepare_event_data(records)

# Check ACLED returns

print(analysis_gdf.crs)
print(analysis_gdf.shape)

# Load Ukraine Oblast boundaries
oblasts = load_boundaries('data/boundaries/geoBoundaries-UKR-ADM1-all/geoBoundaries-UKR-ADM1.geojson')
print(oblasts.head())
print(oblasts.columns)
print(oblasts.crs)
print(f"Number of oblast areas: {len(oblasts)}")
print(oblasts['shapeName'].tolist())

# Calculate oblast areas
oblasts_area = calculate_oblast_areas(oblasts)

# Check the projected coordinate reference system
print(oblasts_area.crs)

# Check oblast area in square kilometres
print(oblasts_area[["shapeName", "area_km2"]].head())

# Assign ACLED event points to Ukraine oblast polygons
events_joined = assign_events_to_oblasts(
    analysis_gdf,
    oblasts
)

# Check join
print(events_joined.shape)
print(events_joined[["shapeName"]].head())

# Check for events not assigned to an oblast
print(events_joined["shapeName"].isna().sum())

# Calculate event counts and density by oblast area
oblast_summary = calculate_event_density(
    events_joined,
    oblasts_area
)

# Check merge
print(oblast_summary.shape)
print(oblast_summary[["shapeName", "area_km2", "event_count"]].head())

# Check for no events
print(oblast_summary["event_count"].isna().sum())

# Replace missing event counts with zero
oblast_summary["event_count"] = oblast_summary["event_count"].fillna(0).astype(int)

# Check replaced with zero
print(oblast_summary["event_count"].isna().sum())

# Calculate reported events per 1,000 square kilometres
oblast_summary["events_per_1000km2"] = (
    oblast_summary["event_count"] / oblast_summary["area_km2"]
) * 1000

print(
    oblast_summary[
        ["shapeName", "event_count", "area_km2", "events_per_1000km2"]
    ].sort_values("events_per_1000km2", ascending=False).head()
)

# Map reported event density
ax = oblast_summary.plot(
    column="events_per_1000km2",
    cmap="RdYlGn_r",
    legend=True,
    edgecolor="black",
    linewidth=0.5,
    figsize=(10, 8),
    legend_kwds={"label": "Events per 1,000 km²"}
)

ax.set_title("Conflict Event Density in Ukraine, 12–18 July 2025")
ax.set_axis_off()

plt.savefig(
    "outputs/ukraine_event_density_12_18_july_2025.png",
    dpi=300,
    bbox_inches="tight"
)

plt.tight_layout()
plt.show()

# Identify the ten oblast areas with the highest event counts
top_10_events = (
    oblast_summary[["shapeName", "event_count"]]
    .sort_values("event_count", ascending=False)
    .head(10)
)

# Check top 10
print(top_10_events)

# Plot the ten oblast areas
top_10_plot = top_10_events.sort_values("event_count")

fig, ax = plt.subplots(figsize=(10, 6))

ax.barh(
    top_10_plot["shapeName"],
    top_10_plot["event_count"]
)
for i, value in enumerate(top_10_plot["event_count"]):
    ax.text(value + 5, i, str(value), va="center")

ax.set_title("Top 10 Oblast Areas by Conflict Events, 12–18 July 2025")
ax.set_xlabel("Event count")
ax.set_ylabel("Oblast area")

plt.tight_layout()
plt.savefig(
    "outputs/top_10_oblast_event_counts_12_18_july_2025.png",
    dpi=300,
    bbox_inches="tight"
)
plt.show()

# Create a summary table of event counts and density by oblast area
summary_table = oblast_summary[[
    "shapeName",
    "event_count",
    "area_km2",
    "events_per_1000km2"
]].copy()
summary_table["area_km2"] = summary_table["area_km2"].round(2)
summary_table["events_per_1000km2"] = summary_table["events_per_1000km2"].round(2)
summary_table = summary_table.sort_values(
    "event_count",
    ascending=False
)
# Check table
print(summary_table.head(10))

# Export oblast area summary table
summary_table.to_csv(
    "outputs/oblast_area_event_summary_12_18_july_2025.csv",
    index=False
)

# Count conflict events by event type
event_type_counts = analysis_gdf["event_type"].value_counts()
print(event_type_counts)

# Plot conflict events by event type
event_type_plot = event_type_counts.sort_values()
fig, ax = plt.subplots(figsize=(9, 5))

ax.barh(
    event_type_plot.index,
    event_type_plot.values
)

ax.set_title("Conflict Events by Event Type, 12–18 July 2025")
ax.set_xlabel("Event count")
ax.set_ylabel("Event type")

for i, value in enumerate(event_type_plot.values):
    ax.text(value + 10, i, str(value), va="center")

ax.set_xlim(0, event_type_plot.max() * 1.1)
plt.tight_layout()
plt.savefig(
    "outputs/event_types_12_18_july_2025.png",
    dpi=300,
    bbox_inches="tight"
)
plt.show()

# Plot ACLED event points over Ukraine administrative boundaries
# ax = oblasts.plot(facecolor="none", edgecolor="black")
# events_gdf.plot(ax=ax, color="red", markersize=30)
# plt.show()
