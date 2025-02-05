# Use the data from "world_series_champions.csv" to append World Series wins and losses to the final dataframe containing all statistics

import pandas as pd

# Load World Series champions data
df1 = pd.read_csv("world_series_champions.csv")

def add_world_series_column(df2):
    """Add a WSwin column indicating if a team won the World Series."""

    # Merge df2 with df1 based on Season and teamIDfg
    df2 = df2.merge(
        df1[['SEASON', 'teamIDfg']],
        left_on=['Season', 'teamIDfg'],
        right_on=['SEASON', 'teamIDfg'],
        how='left',
        indicator=True
    )

    # Create WSwin column (True if a match exists, False otherwise)
    df2['WSwin'] = df2['_merge'] == 'both'

    # Drop unnecessary columns
    df2.drop(columns=['SEASON', '_merge'], inplace=True)

    return df2
