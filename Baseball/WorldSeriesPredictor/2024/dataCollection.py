# hittingStatsFunction.py, pitchingStatsFunction.py, fieldingStatsFunction.py, and world_series_champions.csv are needed in the same project directory as this file in order to run
# This will create a .csv file called "collected_stats.csv" that will contain all team statistics for every year specified

import pandas as pd
from hittingStatsFunction import hitting_stats
from pitchingStatsFunction import pitching_stats
from fieldingStatsFunction import fielding_stats
from wsColumn import add_world_series_column

# Define start and final year (currently collecting stats for only the year 2024)
start_year = 2024 # Enter your own start year
final_year = 2024 # Enter your own end year

# Fetch statistics
df_p = pitching_stats(start_year, final_year)
df_h = hitting_stats(start_year, final_year).drop(columns=['teamIDfg', 'Season', 'Team', 'Age'])
df_f = fielding_stats(start_year, final_year).drop(columns=['teamIDfg', 'Season', 'Team'])

# Merge dataframes
merged_df = pd.concat([df_p, df_h, df_f], axis=1).dropna(axis=1)

# Add World Series column
merged_df = add_world_series_column(merged_df)

# Save and display results
merged_df.to_csv("collected_stats.csv", index=False)
