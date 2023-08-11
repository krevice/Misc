from fanGraphsDataScraperFunction import fg_scrape
import pandas as pd

# Define the dictionary to map team names to team IDs for FANGRAPHS URL
mlb_teams = {
    'Arizona Diamondbacks': 'diamondbacks',
    'Atlanta Braves': 'braves',
    'Baltimore Orioles': 'orioles',
    'Boston Red Sox': 'red-sox',
    'Chicago Cubs': 'cubs',
    'Chicago White Sox': 'white-sox',
    'Cincinnati Reds': 'reds',
    'Cleveland Guardians': 'guardians',
    'Colorado Rockies': 'rockies',
    'Detroit Tigers': 'tigers',
    'Houston Astros': 'astros',
    'Kansas City Royals': 'royals',
    'Los Angeles Angels': 'angels',
    'Los Angeles Dodgers': 'dodgers',
    'Miami Marlins': 'marlins',
    'Milwaukee Brewers': 'brewers',
    'Minnesota Twins': 'twins',
    'New York Mets': 'mets',
    'New York Yankees': 'yankees',
    'Oakland Athletics': 'athletics',
    'Philadelphia Phillies': 'phillies',
    'Pittsburgh Pirates': 'pirates',
    'San Diego Padres': 'padres',
    'San Francisco Giants': 'giants',
    'Seattle Mariners': 'mariners',
    'St. Louis Cardinals': 'cardinals',
    'Tampa Bay Rays': 'rays',
    'Texas Rangers': 'rangers',
    'Toronto Blue Jays': 'blue-jays',
    'Washington Nationals': 'nationals'
}

teams = mlb_teams.values()
years = list(range(2015, 2016))
fg_data_frames = []

for team in teams:
    for year in years:
        team_data = fg_scrape(team, year)

        if team_data is not None:
            fg_data_frames.append(team_data)

fg_data = pd.concat(fg_data_frames, ignore_index=True)

fg_data.to_csv("Fangraphs Data.csv", index=False)
