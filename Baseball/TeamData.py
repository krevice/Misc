# This code should be run to capture the latest MLB team-based statistics
#Excel file is generated to work from to avoid triggering bot protections on baseball-reference.com

import requests
from bs4 import BeautifulSoup
import pandas as pd


list = []
url_list = [
    'https://www.baseball-reference.com/teams/ARI/',
    'https://www.baseball-reference.com/teams/ATL/',
    'https://www.baseball-reference.com/teams/BAL/',
    'https://www.baseball-reference.com/teams/BOS/',
    'https://www.baseball-reference.com/teams/CHW/',
    'https://www.baseball-reference.com/teams/CHC/',
    'https://www.baseball-reference.com/teams/CIN/',
    'https://www.baseball-reference.com/teams/CLE/',
    'https://www.baseball-reference.com/teams/COL/',
    'https://www.baseball-reference.com/teams/DET/',
    'https://www.baseball-reference.com/teams/HOU/',
    'https://www.baseball-reference.com/teams/KCR/',
    'https://www.baseball-reference.com/teams/ANA/',
    'https://www.baseball-reference.com/teams/LAD/',
    'https://www.baseball-reference.com/teams/FLA/',
    'https://www.baseball-reference.com/teams/MIL/',
    'https://www.baseball-reference.com/teams/MIN/',
    'https://www.baseball-reference.com/teams/NYY/',
    'https://www.baseball-reference.com/teams/NYM/',
    'https://www.baseball-reference.com/teams/OAK/',
    'https://www.baseball-reference.com/teams/PHI/',
    'https://www.baseball-reference.com/teams/PIT/',
    'https://www.baseball-reference.com/teams/SDP/',
    'https://www.baseball-reference.com/teams/SFG/',
    'https://www.baseball-reference.com/teams/SEA/',
    'https://www.baseball-reference.com/teams/STL/',
    'https://www.baseball-reference.com/teams/TBD/',
    'https://www.baseball-reference.com/teams/TEX/',
    'https://www.baseball-reference.com/teams/TOR/',
    'https://www.baseball-reference.com/teams/WSN/'
]

for url in url_list:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    team_table = soup.find_all('table')[0]
    df = pd.read_html(str(team_table))[0].iloc[0]
    df_dict = df.to_dict()
    df_dict = {key: value.replace('\xa0', ' ') if isinstance(value, str) else value for key, value in df_dict.items()}
    list.append(df_dict)

df = pd.DataFrame(list)

df.to_csv('team_df.csv', index=False)
