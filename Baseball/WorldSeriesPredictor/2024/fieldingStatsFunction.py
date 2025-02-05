from pybaseball import team_fielding

def fielding_stats(syear, fyear):
    """Retrieve and format team fielding statistics from PyBaseball."""

    exclude_cols = {'teamIDfg', 'Season', 'Team', 'Age'}  # Use a set for faster lookups

    # Fetch team fielding stats
    df_f = team_fielding(syear, fyear)

    # Rename columns with "(F)" prefix, excluding specified columns
    df_f.rename(columns=lambda col: f"(F) {col}" if col not in exclude_cols else col, inplace=True)

    # Sort and reset index
    df_f.sort_values(['teamIDfg', 'Season'], ascending=True, inplace=True)
    df_f.reset_index(drop=True, inplace=True)

    return df_f
