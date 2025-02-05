from pybaseball import team_batting

def hitting_stats(syear, fyear):
    """Retrieve and format team batting statistics from PyBaseball."""

    exclude_cols = {'teamIDfg', 'Season', 'Team', 'Age'}  # Use a set for faster lookups

    # Fetch team batting stats
    df_h = team_batting(syear, fyear)

    # Rename columns with "(H)" prefix, excluding specified columns
    df_h.rename(columns=lambda col: f"(H) {col}" if col not in exclude_cols else col, inplace=True)

    # Sort and reset index
    df_h.sort_values(['teamIDfg', 'Season'], ascending=True, inplace=True)
    df_h.reset_index(drop=True, inplace=True)

    return df_h
