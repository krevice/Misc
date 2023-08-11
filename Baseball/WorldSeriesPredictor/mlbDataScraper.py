import requests
from bs4 import BeautifulSoup
import pandas as pd

def savant_scrape(team_id, year):
    # Define the dictionary to map team names to team IDs for BASEBALL SAVANT URL
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

########### Capture Statcast tables for MLB team in a season ###########

    base_url = 'https://baseballsavant.mlb.com/team/{}/?season={}'
    url = base_url.format(team_id, year)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    try:
        # Find all tables on the page
        savant_table = soup.find_all('table')

        if not savant_table:
            team_name = next((name for name, id in mlb_teams.items() if id == team_id), 'Unknown Team')
            print(f"No tables found for {team_name} in {year}")
            return None

######################## Extract Statcast hitting data ############################

        # Read hitting data from the first table
        df_hitting = pd.read_html(str(savant_table))[0]

        # Clean up hitting DataFrame columns
        df_hitting.columns = df_hitting.columns.droplevel(0)  # Remove the top-level column header
        df_hitting = df_hitting.rename_axis(None, axis=1)  # Remove the name of the columns axis

        # Keep only the second-to-last row of hitting data for team averages
        df_hitting = df_hitting.iloc[-2:-1]

        # Rename the 'Player' column to 'Team' in hitting data
        df_hitting.rename(columns={'Player': 'Team'}, inplace=True)

        # Remove the very last column from the hitting data
        df_hitting = df_hitting.iloc[:, :-1]

####################### Extract Statcast plate discipline data ##########################

        # Read plate discipline data from the second table
        df_discipline = pd.read_html(str(savant_table))[1]

        # Clean up plate discipline DataFrame columns
        df_discipline.reset_index(drop=True, inplace=True)
        df_discipline = df_discipline.iloc[:, :-1]

        # Keep only the second-to-last row of plate discipline data
        df_discipline = df_discipline.iloc[-2:-1]

        # Remove the first two columns from discipline data
        df_discipline = df_discipline.iloc[:, 2:]

        # Combine hitting and plate discipline data
        combined_data = pd.concat([df_hitting, df_discipline], axis=1)

################## Extract Statcast batted ball profile data ########################

        # Read plate discipline data from the second table
        df_bbprofile = pd.read_html(str(savant_table))[2]

        # Clean up plate discipline DataFrame columns
        df_bbprofile.reset_index(drop=True, inplace=True)
        df_bbprofile = df_bbprofile.iloc[:, :-1]

        # Keep only the second-to-last row of plate discipline data
        df_bbprofile = df_bbprofile.iloc[-2:-1]

        ## Remove the first two columns from batted ball profile data
        df_bbprofile = df_discipline.iloc[:, 2:]

        # Combine hitting and plate discipline data
        combined_data = pd.concat([df_hitting, df_discipline, df_bbprofile], axis=1)

#################### Extract Division Rank from Statcast ########################

        # Find and extract 'Division Rank'
        division_rank_element = soup.find(class_="box-title", string="Division Rank")
        division_rank = division_rank_element.find_next_sibling("div").get_text(strip=True)
        division_rank = ''.join(filter(str.isdigit, division_rank))
        combined_data['Division Rank'] = division_rank

######################## Extract Run Differential from Statcast ########################

        # Find and extract 'Run Differential'
        run_diff_element = soup.find(class_="box-title", string="Run Differential")
        run_diff = run_diff_element.find_next_sibling("div").get_text(strip=True)
        combined_data['Run Differential'] = run_diff

######################### Extract Fangraphs tables #######################



        return combined_data

    except Exception as e:
        print(f"An error occurred for {team_id} in {year}: {e}")
        return None
