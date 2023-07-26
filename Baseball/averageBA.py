# this function takes the Batting Game Log page from baseball-reference.com as input

import requests
from bs4 import BeautifulSoup
import pandas as pd

def averageBA(playerProfile):

# define regex
    months_regex_dict = {
        "January": r"Jan \d+",
        "February": r"Feb \d+",
        "March": r"Mar \d+",
        "April": r"Apr \d+",
        "May": r"May \d+",
        "June": r"Jun \d+",
        "July": r"Jul \d+",
        "August": r"Aug \d+",
        "September": r"Sep \d+",
        "October": r"Oct \d+",
        "November": r"Nov \d+",
        "December": r"Dec \d+"
    }

## Data for Bailey ##
    url = playerProfile
    response = requests.get(url)

# Capture HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

# extract the batting average table
    tables_player = soup.find_all('table')[4]

# Convert table to data frame, remove the last row
    df_player = pd.read_html(str(tables_player))[0]
    df_player['AB'] = pd.to_numeric(df_player['AB'], errors='coerce')
    df_player = df_player.dropna(subset=['AB'])
    df_player['H'] = pd.to_numeric(df_player['H'], errors='coerce')
    df_player = df_player.dropna(subset=['H'])
    df_player = df_player.dropna(subset=['Date'])

    average_ba_list = []
    for month, regex_pattern in months_regex_dict.items():
        month_df = df_player[df_player['Date'].str.contains(regex_pattern, regex=True)]
        if month_df['AB'].sum() >= 10:
            average_ba = month_df['H'].sum() / month_df['AB'].sum()
            average_ba_list.append({'Month': month, 'Average_BA': average_ba})
        else:
            continue

    average_ba_df = pd.DataFrame(average_ba_list)

    return(average_ba_df)
