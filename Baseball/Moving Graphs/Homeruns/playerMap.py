from pybaseball import standings
from pybaseball import statcast
import seaborn as sns
import matplotlib.pyplot as plt
import datetime
import pandas as pd
from collections import defaultdict
import bar_chart_race as bcr
import imageio
from matplotlib.animation import FuncAnimation

# Query and filter data by team
##data.to_csv('statcast_2023.csv')

mlbid_map = pd.read_csv('razzball.csv')

# Convert DataFrame to dictionary
name_mlbamid_dict = {}
for index, row in mlbid_map.iterrows():
    name_mlbamid_dict[row["Name"]] = row["MLBAMID"]

# Swap keys and values within the dictionary
name_mlbamid_dict = {v: k for k, v in name_mlbamid_dict.items()}

data = pd.read_csv('statcast_2023.csv')

# Replace specific values in 'batter' column with modified string representation
data['batter'] = data['batter'].map(name_mlbamid_dict)

data = data[data['events'] == 'home_run']
home_run_data = data[['game_date', 'batter', 'events']]
home_run_data.to_csv('statcast_test2.csv')
