import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import concurrent.futures
from tqdm import tqdm


def fg_scrape(team: str, year: int) -> pd.DataFrame:
    """
    Scrapes FanGraphs team statistics for a given team and season.

    Parameters:
        team (str): Team name slug for the URL.
        year (int): Season year to scrape data for.

    Returns:
        pd.DataFrame: A dataframe containing hitting, pitching, and fielding stats.
    """
    base_url = f'https://www.fangraphs.com/teams/{team}/stats?season={year}'

    try:
        response = requests.get(base_url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Locate all tables on the page
        tables = soup.find_all('table')
        if not tables:
            print(f"No table found for {team} ({year})")
            return None

        # Extract statistics from the respective tables
        df_hitting = pd.read_html(str(tables[8]))[0].iloc[:, 5:].iloc[-1:].reset_index(drop=True)
        df_hitting = df_hitting.applymap(lambda x: x.replace('%', '') if isinstance(x, str) else x)

        df_spitcher = pd.read_html(str(tables[9]))[0].iloc[:, 5:].iloc[-1:].reset_index(drop=True)
        df_rpitcher = pd.read_html(str(tables[10]))[0].iloc[:, 5:].iloc[-1:].reset_index(drop=True)
        df_defense = pd.read_html(str(tables[11]))[0].iloc[-1:][
            ['DRS', 'RngR', 'ErrR', 'UZR', 'UZR/150', 'Def']].reset_index(drop=True)

        # Rename columns with appropriate prefixes
        df_spitcher.columns = ['S_Pitcher_' + col for col in df_spitcher.columns]
        df_rpitcher.columns = ['R_Pitcher_' + col for col in df_rpitcher.columns]
        df_defense.columns = ['Fielding_' + col for col in df_defense.columns]

        # Extract team name and season from the webpage
        team_name_element = soup.find('h1', class_='team-name')
        if not team_name_element:
            print(f"Could not extract team name for {team} ({year})")
            return None

        team_name = team_name_element.text.strip()
        season_match = re.search(r'\d{4}', team_name)
        season = season_match.group() if season_match else str(year)
        team_name = re.sub(r'\d', '', team_name).strip()

        df_hitting.insert(0, 'Team', team_name)
        df_hitting.insert(1, 'Season', season)

        # Combine all data into a single dataframe
        return pd.concat([df_hitting, df_spitcher, df_rpitcher, df_defense], axis=1)

    except requests.exceptions.RequestException as e:
        print(f"Request error for {team} ({year}): {e}")
    except Exception as e:
        print(f"Error processing {team} ({year}): {e}")

    return None


def scrape_all_teams(start_year: int, end_year: int = None, team: str = 'all') -> pd.DataFrame:
    """
    Scrapes FanGraphs data for all or a specific MLB team over a range of seasons.

    Parameters:
        start_year (int): The first season to scrape.
        end_year (int, optional): The last season to scrape. Defaults to start_year.
        team (str, optional): Specific team name to scrape, or 'all' for all teams.

    Returns:
        pd.DataFrame: Combined dataframe of all scraped teams and seasons.
    """
    mlb_teams = {
        'Arizona Diamondbacks': 'diamondbacks', 'Atlanta Braves': 'braves', 'Baltimore Orioles': 'orioles',
        'Boston Red Sox': 'red-sox', 'Chicago Cubs': 'cubs', 'Chicago White Sox': 'white-sox',
        'Cincinnati Reds': 'reds', 'Cleveland Guardians': 'guardians', 'Colorado Rockies': 'rockies',
        'Detroit Tigers': 'tigers', 'Houston Astros': 'astros', 'Kansas City Royals': 'royals',
        'Los Angeles Angels': 'angels', 'Los Angeles Dodgers': 'dodgers', 'Miami Marlins': 'marlins',
        'Milwaukee Brewers': 'brewers', 'Minnesota Twins': 'twins', 'New York Mets': 'mets',
        'New York Yankees': 'yankees', 'Oakland Athletics': 'athletics', 'Philadelphia Phillies': 'phillies',
        'Pittsburgh Pirates': 'pirates', 'San Diego Padres': 'padres', 'San Francisco Giants': 'giants',
        'Seattle Mariners': 'mariners', 'St. Louis Cardinals': 'cardinals', 'Tampa Bay Rays': 'rays',
        'Texas Rangers': 'rangers', 'Toronto Blue Jays': 'blue-jays', 'Washington Nationals': 'nationals'
    }

    end_year = end_year or start_year
    if end_year < start_year:
        print("Error: end_year cannot be earlier than start_year.")
        return None

    # Normalize team names for case-insensitive matching
    team_normalized = {k.lower(): v for k, v in mlb_teams.items()}

    if team.lower() == 'all':
        teams = list(mlb_teams.values())
    else:
        if team.lower() not in team_normalized:
            print(f"Error: '{team}' is not a valid team.")
            return None
        teams = [team_normalized[team.lower()]]

    # Prepare a list of tasks for concurrent scraping
    tasks = [(t, year) for year in range(start_year, end_year + 1) for t in teams]
    scraped_data = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(fg_scrape, team, year): (team, year) for team, year in tasks}

        for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures), desc="Scraping Data"):
            try:
                result = future.result()
                if result is not None:
                    scraped_data.append(result)
            except Exception as e:
                t, y = futures[future]
                print(f"Error scraping {t} for {y}: {e}")

    if scraped_data:
        final_df = pd.concat(scraped_data, ignore_index=True)
        final_df.sort_values(by=['Team', 'Season'], ascending=True, inplace=True)
        return final_df

    print("No data was scraped.")
    return None
