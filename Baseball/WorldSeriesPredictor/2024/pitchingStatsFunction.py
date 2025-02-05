from pybaseball import team_pitching

def pitching_stats(syear, fyear):
    """Retrieve and format team pitching statistics from PyBaseball."""

    exclude_cols = {'teamIDfg', 'Season', 'Team', 'Age'}  # Use a set for faster lookups

    # Fetch team pitching stats
    df_p = team_pitching(syear, fyear)

    # Rename columns with "(P)" prefix, excluding specified columns
    df_p.rename(columns=lambda col: f"(P) {col}" if col not in exclude_cols else col, inplace=True)

    # Sort and reset index
    df_p.sort_values(['teamIDfg', 'Season'], ascending=True, inplace=True)
    df_p.reset_index(drop=True, inplace=True)

    return df_p
