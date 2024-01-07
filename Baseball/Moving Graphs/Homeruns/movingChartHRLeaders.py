import bar_chart_race as bcr
import pandas as pd

# Use .csv created from playerMod.py 
df = pd.read_csv('statcast_mod.csv')

# Convert game_date to datetime
df['game_date'] = pd.to_datetime(df['game_date'])
pivot_df = df.pivot_table(index='game_date', columns='batter', values='events', aggfunc='count', fill_value=0)
pivot_df = pivot_df.astype(float)
pivot_df.to_csv('testing.csv')
pivot_df = pivot_df.cumsum()

# Reformatting the DataFrame
print(pivot_df)

df = pivot_df
bcr.bar_chart_race(
    df=df,
    filename='homeruns.gif',
    orientation='h',
    sort='desc',
    n_bars=10,
    fixed_order=False,
    fixed_max=True,
    steps_per_period=5,
    interpolate_period=False,
    label_bars=True,
    bar_size=.95,
    period_label={'x': .99, 'y': .25, 'ha': 'right', 'va': 'center'},
    period_fmt='%B %d, %Y',
    period_summary_func=lambda v, r: {'x': .99, 'y': .18,
                                      's': '',
                                      'ha': 'right', 'size': 8, 'family': 'Courier New'},
    period_length=10,
    figsize=(5, 3),
    dpi=144,
    cmap='dark12',
    title='MLB Homerun Leaders (2023)',
    title_size='',
    bar_label_size=7,
    tick_label_size=7,
    shared_fontdict={'family' : 'Helvetica', 'color' : '.1'},
    scale='linear',
    writer=None,
    fig=None,
    bar_kwargs={'alpha': .7},
    filter_column_colors=False)
