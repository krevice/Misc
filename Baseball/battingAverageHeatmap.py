# this code will generate a heatmap displaying player batting averages through the season
# currently this code is set to display the batting averages of SF Giants position players

from averageBA import averageBA
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

baileyBA = averageBA('https://www.baseball-reference.com/players/gl.fcgi?id=bailepa01&t=b&year=2023')
confortoBA = averageBA('https://www.baseball-reference.com/players/gl.fcgi?id=confomi01&t=b&year=2023')
crawfordBA = averageBA('https://www.baseball-reference.com/players/gl.fcgi?id=crawfbr01&t=b&year=2023')
davisBA = averageBA('https://www.baseball-reference.com/players/gl.fcgi?id=davisjd01&t=b&year=2023')
floresBA = averageBA('https://www.baseball-reference.com/players/gl.fcgi?id=florewi01&t=b&year=2023')
matosBA = averageBA('https://www.baseball-reference.com/players/gl.fcgi?id=matoslu02&t=b&year=2023')
pedersonBA = averageBA('https://www.baseball-reference.com/players/gl.fcgi?id=pederjo01&t=b&year=2023')
sabolBA = averageBA('https://www.baseball-reference.com/players/gl.fcgi?id=sabolbl01&t=b&year=2023')
slaterBA  =averageBA('https://www.baseball-reference.com/players/gl.fcgi?id=slateau01&t=b&year=2023')
schmittBA = averageBA('https://www.baseball-reference.com/players/gl.fcgi?id=schmica01&t=b&year=2023')
wadeBA = averageBA('https://www.baseball-reference.com/players/gl.fcgi?id=wadela01&t=b&year=2023')
wiselyBA = averageBA('https://www.baseball-reference.com/players/gl.fcgi?id=wiselbr01&t=b&year=2023')
yazBA = averageBA('https://www.baseball-reference.com/players/gl.fcgi?id=yastrmi01&t=b&year=2023')

merge = pd.concat([
    baileyBA.set_index('Month').rename(columns={'Average_BA': 'Bailey'}),
    confortoBA.set_index('Month').rename(columns={'Average_BA': 'Conforto'}),
    crawfordBA.set_index('Month').rename(columns={'Average_BA': 'Crawford'}),
    davisBA.set_index('Month').rename(columns={'Average_BA': 'Davis'}),
    floresBA.set_index('Month').rename(columns={'Average_BA': 'Flores'}),
    matosBA.set_index('Month').rename(columns={'Average_BA': 'Matos'}),
    pedersonBA.set_index('Month').rename(columns={'Average_BA': 'Pederson'}),
    sabolBA.set_index('Month').rename(columns={'Average_BA': 'Sabol'}),
    schmittBA.set_index('Month').rename(columns={'Average_BA': 'Schmitt'}),
    slaterBA.set_index('Month').rename(columns={'Average_BA': 'Slater'}),
    wadeBA.set_index('Month').rename(columns={'Average_BA': 'Wade'}),
    wiselyBA.set_index('Month').rename(columns={'Average_BA': 'Wiseley'}),
    yazBA.set_index('Month').rename(columns={'Average_BA': 'Yaz'}),
], axis=1)

month_order = ['July', 'June', 'May', 'April']
merge = merge.reindex(month_order)

plt.figure(figsize=(15, 8))
heatmap = sns.heatmap(merge, annot=True, cmap="coolwarm", fmt=".3f", cbar=True, cbar_kws={'format': '%.3f'})
plt.title("Monthly Batting Averages (min. 10 ABs)")
heatmap.set_xlabel("Players", labelpad=20)
heatmap.set_ylabel("Month of 2023 Season", labelpad=20)
plt.show()
