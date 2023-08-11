from savantDataScraperFunction import savant_scrape
import pandas as pd

# Define the dictionary to map team names to team IDs on baseball savant
mlb_teams = {
    'Arizona Diamondbacks': 109,
    'Atlanta Braves': 144,
    'Baltimore Orioles': 110,
    'Boston Red Sox': 111,
    'Chicago Cubs': 112,
    'Chicago White Sox': 145,
    'Cincinnati Reds': 113,
    'Cleveland Guardians': 114,
    'Colorado Rockies': 115,
    'Detroit Tigers': 116,
    'Houston Astros': 117,
    'Kansas City Royals': 118,
    'Los Angeles Angels': 108,
    'Los Angeles Dodgers': 119,
    'Miami Marlins': 146,
    'Milwaukee Brewers': 158,
    'Minnesota Twins': 142,
    'New York Mets': 121,
    'New York Yankees': 147,
    'Oakland Athletics': 133,
    'Philadelphia Phillies': 143,
    'Pittsburgh Pirates': 134,
    'San Diego Padres': 135,
    'San Francisco Giants': 137,
    'Seattle Mariners': 136,
    'St. Louis Cardinals': 138,
    'Tampa Bay Rays': 139,
    'Texas Rangers': 140,
    'Toronto Blue Jays': 141,
    'Washington Nationals': 120
}

# Change to appropriate baseball savant indexes
team_ids = mlb_teams.values()
#team_names = sorted(mlb_teams.keys())
years = list(range(2015, 2017))  # Years from 2015 to 2022

# Initialize an empty list to hold DataFrames
savant_data_frames = []

# Loop through each team ID
for team_id in team_ids:
    # Loop through each year for the current team
    for year in years:
        team_data = savant_scrape(team_id, year)  # Convert year to string

        if team_data is not None:
            savant_data_frames.append(team_data)

# Combine all DataFrames in the list into a single DataFrame
savant_data = pd.concat(savant_data_frames, ignore_index=True)

# Now you have the combined DataFrame with data for all teams and years
savant_data.to_csv("Savant Data.csv", index=False)
