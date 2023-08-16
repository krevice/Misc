import requests                  # Import the requests library for making HTTP requests
from bs4 import BeautifulSoup   # Import BeautifulSoup for parsing HTML content
import pandas as pd             # Import pandas for data manipulation and analysis
import time                     # Import the time module for adding delays

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

# Define the base URL for team and season data
    base_url = 'https://baseballsavant.mlb.com/team/{}/?season={}'

    while True:
        # Construct the URL with the provided team ID and year
        url = base_url.format(team_id, year)
        response = requests.get(url)                # Send an HTTP GET request to the URL
        soup = BeautifulSoup(response.content, 'html.parser')  # Parse the HTML content using BeautifulSoup

        try:
            # Find all tables on the page
            savant_table = soup.find_all('table')   # Find all HTML tables on the page

            if not savant_table:
                # If no tables are found, print a message and retry after a delay
                team_name = next((name for name, id in mlb_teams.items() if id == team_id), 'Unknown Team')
                print(f"No tables found for {team_name} in {year}")
                time.sleep(5)  # Add a delay before retrying

            else:
                # Extract Statcast hitting data
                df_hitting = pd.read_html(str(savant_table))[0]  # Read the first table as a DataFrame
                df_hitting.columns = df_hitting.columns.droplevel(0)  # Remove top-level column header
                df_hitting = df_hitting.rename_axis(None, axis=1)  # Remove column axis name
                df_hitting = df_hitting.iloc[-2:-1]  # Keep second-to-last row
                df_hitting.rename(columns={'Player': 'Team'}, inplace=True)  # Rename 'Player' column
                df_hitting = df_hitting.iloc[:, :-1]  # Remove last column

                # Extract Statcast plate discipline data
                df_discipline = pd.read_html(str(savant_table))[1]  # Read the second table as a DataFrame
                df_discipline.reset_index(drop=True, inplace=True)  # Reset index and update DataFrame
                df_discipline = df_discipline.iloc[-2:-1]  # Keep second-to-last row
                df_discipline = df_discipline.iloc[:, 2:]  # Remove first two columns

                # Extract Statcast batted ball profile data
                df_bbprofile = pd.read_html(str(savant_table))[2]  # Read the third table as a DataFrame
                df_bbprofile.reset_index(drop=True, inplace=True)  # Reset index and update DataFrame
                df_bbprofile = df_bbprofile.iloc[:, :-1]  # Remove last column
                df_bbprofile = df_bbprofile.iloc[-2:-1]  # Keep second-to-last row
                df_bbprofile = df_bbprofile.iloc[:, 2:]  # Remove first two columns

                # Combine hitting, plate discipline, and batted ball profile data
                combined_data = pd.concat([df_hitting, df_discipline, df_bbprofile], axis=1)

                # Extract Division Rank from Statcast
                division_rank_element = soup.find(class_="box-title", string="Division Rank")
                division_rank = division_rank_element.find_next_sibling("div").get_text(strip=True)
                division_rank = ''.join(filter(str.isdigit, division_rank))
                combined_data['Division Rank'] = division_rank

                # Extract Run Differential from Statcast
                run_diff_element = soup.find(class_="box-title", string="Run Differential")
                run_diff = run_diff_element.find_next_sibling("div").get_text(strip=True)
                combined_data['Run Differential'] = run_diff

                # Return the combined data
                return combined_data

        except Exception as e:
            # Handle exceptions and print an error message
            print(f"An error occurred for {team_id} in {year}: {e}")
            return None
