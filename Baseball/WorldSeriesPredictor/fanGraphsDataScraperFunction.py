import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

def fg_scrape(team, years):
# Define the dictionary to map team names to team IDs for BASEBALL SAVANT URL
    mlb_teams = {
        'Arizona Diamondbacks': 'diamondbacks',
        'Atlanta Braves': 'braves'
    }

########### Capture Fangraphs tables for MLB team in a season ###########

    base_url = 'https://www.fangraphs.com/teams/{}/stats?season={}'
    url = base_url.format(team, years)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    fg_table = soup.find_all('table')

    df_hitting = pd.read_html(str(fg_table))[5]

    df_hitting = df_hitting.iloc[:, 5:]

    df_hitting = df_hitting.iloc[-1:]

    columns_to_remove = ['AVG', 'OBP', 'SLG', 'wOBA']
    df_hitting = df_hitting.drop(columns=columns_to_remove)

    df_hitting.columns = ['FG_Batter_' + col for col in df_hitting.columns]

    df_hitting = df_hitting.applymap(lambda x: x.replace('%', '') if isinstance(x, str) else x)

    df_hitting = df_hitting.reset_index(drop=True)

# Extract team name from the h1 tag
    team_name = soup.find('h1', class_='team-name').text.strip()

# Extract the year from the team name using regular expression
    season = re.search(r'\d{4}', team_name).group()

# Remove the year information
    team_name = re.sub(r'\d', '', team_name).strip()

    df_hitting.insert(0, 'Team', team_name)
    df_hitting.insert(1, 'Season', season)

####################### Extract Fangraphs pitching data ##########################

    df_spitcher = pd.read_html(str(fg_table))[6]

    df_spitcher = df_spitcher.iloc[:, 5:]

    df_spitcher = df_spitcher.iloc[-1:]

    df_spitcher.columns = ['FG_S_Pitcher_' + col for col in df_spitcher.columns]

    df_spitcher = df_spitcher.applymap(lambda x: x.replace('%', '') if isinstance(x, str) else x)

    df_spitcher = df_spitcher.reset_index(drop=True)

############### Extract Fangraphs relief pitcher data ####################

    df_rpitcher = pd.read_html(str(fg_table))[7]

    df_rpitcher = df_rpitcher.iloc[:, 5:]

    df_rpitcher = df_rpitcher.iloc[-1:]

    df_rpitcher.columns = ['FG_R_Pitcher_' + col for col in df_rpitcher.columns]

    df_rpitcher = df_rpitcher.applymap(lambda x: x.replace('%', '') if isinstance(x, str) else x)

    df_rpitcher = df_rpitcher.reset_index(drop=True)

############### Extract Fangraphs defense data ####################

    df_defense = pd.read_html(str(fg_table))[8]

    df_defense = df_defense.iloc[-1:]

    df_defense = df_defense[['DRS', 'RngR', 'ErrR', 'UZR', 'UZR/150', 'Def']]

    df_defense.columns = ['FG_Fielding_' + col for col in df_defense.columns]

    df_defense = df_defense.reset_index(drop=True)

    combined_data = pd.concat([df_hitting, df_spitcher, df_rpitcher, df_defense], axis=1)

    return combined_data
