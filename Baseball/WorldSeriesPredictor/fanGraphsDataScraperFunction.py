import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

def fg_scrape(team, years):
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

# Build the FANGRAPHS URL for the specified team and season
    base_url = 'https://www.fangraphs.com/teams/{}/stats?season={}'.format(mlb_teams[team], years)
    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    fg_table = soup.find_all('table')

    # Extract hitting data
    df_hitting = pd.read_html(str(fg_table))[5]
    df_hitting = df_hitting.iloc[:, 5:]
    df_hitting = df_hitting.iloc[-1:]
    columns_to_remove = ['AVG', 'OBP', 'SLG', 'wOBA']
    df_hitting = df_hitting.drop(columns=columns_to_remove)
    df_hitting.columns = ['FG_Batter_' + col for col in df_hitting.columns]
    df_hitting = df_hitting.applymap(lambda x: x.replace('%', '') if isinstance(x, str) else x)
    df_hitting = df_hitting.reset_index(drop=True)

    # Extract team name and season
    team_name = soup.find('h1', class_='team-name').text.strip()
    season = re.search(r'\d{4}', team_name).group()
    team_name = re.sub(r'\d', '', team_name).strip()
    df_hitting.insert(0, 'Team', team_name)
    df_hitting.insert(1, 'Season', season)

    # Extract starting pitching data
    df_spitcher = pd.read_html(str(fg_table))[6]
    df_spitcher = df_spitcher.iloc[:, 5:]
    df_spitcher = df_spitcher.iloc[-1:]
    df_spitcher.columns = ['FG_S_Pitcher_' + col for col in df_spitcher.columns]
    df_spitcher = df_spitcher.applymap(lambda x: x.replace('%', '') if isinstance(x, str) else x)
    df_spitcher = df_spitcher.reset_index(drop=True)

    # Extract relief pitcher data
    df_rpitcher = pd.read_html(str(fg_table))[7]
    df_rpitcher = df_rpitcher.iloc[:, 5:]
    df_rpitcher = df_rpitcher.iloc[-1:]
    df_rpitcher.columns = ['FG_R_Pitcher_' + col for col in df_rpitcher.columns]
    df_rpitcher = df_rpitcher.applymap(lambda x: x.replace('%', '') if isinstance(x, str) else x)
    df_rpitcher = df_rpitcher.reset_index(drop=True)

    # Extract defense data
    df_defense = pd.read_html(str(fg_table))[8]
    df_defense = df_defense.iloc[-1:]
    df_defense = df_defense[['DRS', 'RngR', 'ErrR', 'UZR', 'UZR/150', 'Def']]
    df_defense.columns = ['FG_Fielding_' + col for col in df_defense.columns]
    df_defense = df_defense.reset_index(drop=True)

    # Combine all the extracted data into a single DataFrame
    combined_data = pd.concat([df_hitting, df_spitcher, df_rpitcher, df_defense], axis=1)

    return combined_data
