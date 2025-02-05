# Create a .csv file containing team IDs, a way to track teams throughout the years (needed due to team name or location changes)
# These IDs then had to be manually added to the .csv file generated from worldSeriesWinnersTable.py to create the file "world_series_champions.csv"

import pandas as pd
from pybaseball import team_ids

# Fetch team IDs
df = pd.DataFrame(team_ids())

# Select relevant columns and drop duplicates
df_unique = df[['franchID', 'teamIDfg']].drop_duplicates(subset='teamIDfg')

# Save to CSV
df_unique.to_csv('teamID.csv', index=False)
