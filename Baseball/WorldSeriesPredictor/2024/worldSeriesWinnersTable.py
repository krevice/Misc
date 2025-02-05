# Create a .csv table for what team won the world series in what year

import pandas as pd

# URL of the World Series winners page
url = "https://www.espn.com/mlb/worldseries/history/winners"

# Read the table from the webpage
df = pd.read_html(url)[0]

# Set the first row as column headers and drop it from the data
df.columns = df.iloc[1]
df = df.iloc[2:].reset_index(drop=True)

# Drop unnecessary columns
df.drop(columns=['LOSER', 'SERIES'], inplace=True)

# Save to CSV file
df.to_csv('world_series.csv', index=False)

# Display the first few rows
print(df.head())
