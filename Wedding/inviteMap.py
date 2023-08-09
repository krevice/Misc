import pandas as pd
import plotly.express as px
from zip2latlong import get_lat_long  # A custom function to get latitude and longitude for a given zip code
import plotly.offline as pyo  # This library is used to save the plot as an HTML file

# Read the data from a CSV file and select relevant columns
df = pd.read_csv('guest_list.csv')
df = df[['First Name', 'Last Name', 'Zip/Postal Code', 'State/Province', 'Country', 'Wedding Day - RSVP']]

# Filter the DataFrame to include only entries from the United States
df = df[df['Country'] == 'United States']

# Extract the 'Zip/Postal Code' column from the DataFrame and convert it to a list
#ziplist = df[['Zip/Postal Code']].values.tolist()

# Flatten the list of lists that was created above
#ziplist = [item for sublist in ziplist for item in sublist]

# Add new columns for Latitude, Longitude, and City to the DataFrame using the 'get_lat_long' function
df["Latitude"], df["Longitude"], df["City"] = zip(*df["Zip/Postal Code"].apply(get_lat_long))

# Create a bubble map using Plotly Express
fig = px.scatter_geo(
    df,
    lat="Latitude",
    lon="Longitude",
    custom_data=["City"],  # Set the custom data for hover text
    scope="usa",  # Show only the United States map
    title="Locations of People Invited to the Wedding",
    projection="albers usa",  # Use the Albers USA projection for the map
    color="State/Province",  # Color the bubbles based on the state/province
    color_discrete_sequence=px.colors.qualitative.Dark24  # Use a custom color palette
)

# Set the hover template to show the City name when hovering over the bubbles
fig.update_traces(hovertemplate="City: %{customdata[0]}")

# Update the marker size for the bubbles
fig.update_traces(marker=dict(size=10))

# Save the plot as an HTML file called 'wedding_invites.html'
pyo.plot(fig, filename='wedding_invites.html', auto_open=False)

# Show the bubble map
fig.show()
