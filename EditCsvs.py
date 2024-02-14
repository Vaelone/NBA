import pandas as pd
from bs4 import BeautifulSoup
# from playwright.sync_api import sync_playwright,TimeoutError as PlaywrightTimeout
import time
import requests
from datetime import datetime
import urllib
import numpy as np

Player23 = pd.read_csv('Players23.csv')
data2 = pd.read_csv('rawodds.csv')

awayTeams = data2['AwayTeam'].unique()
homeTeams = data2['HomeTeam'].unique()

mask = (pd.isna(data2['AwayTeam']) & pd.isna(data2['HomeTeam']))
indices_to_update = data2.index[mask]

for index in indices_to_update:
    name = data2.loc[index, 'participant_name']
    PlayerRow = Player23[Player23['PLAYER'].str.lower() == name.lower()]
    if not PlayerRow.empty:
        Team1 = PlayerRow['TEAM'].iloc[0]
    else:
        print(name)

    if Team1 in awayTeams:
        data2.loc[index, 'AwayTeam'] = Team1
        teamindex = np.argmax(awayTeams == Team1)
        data2.loc[index, 'HomeTeam'] = homeTeams[teamindex]
    elif Team1 in homeTeams:
        data2.loc[index, 'HomeTeam'] = Team1
        teamindex = np.argmax(homeTeams == Team1)
        data2.loc[index, 'AwayTeam'] = awayTeams[teamindex]
# for index, row in data2.iterrows():
#     if (pd.isna(row['AwayTeam']) and pd.isna(row['HomeTeam'])):
#         name = row['participant_name']
#         PlayerRow = Player23[Player23['PLAYER'].str.lower() == name.lower()]
#         Team1 = PlayerRow['TEAM'].iloc[0]
#         index = 0
#         check = False
#         for i in range(len(awayTeams)):
#             if(Team1 == awayTeams[i]):
#                 check=True
#                 break
#             index+=1
#         if(check):
#             data2.loc[index, 'AwayTeam'] = awayTeams[i]
#             data2.loc[index, 'HomeTeam'] = Team1
#         check2 = False
#         for i in range(len(homeTeams)):
#             if(Team1 == homeTeams[i]):
#                 check2=True
#                 break
#             index+=1
#         if(check2):
#             data2.loc[index, 'HomeTeam'] = homeTeams[i]
#             data2.loc[index, 'AwayTeam'] = Team1
print(data2)
# data2.to_csv('resultsedited.csv', index=False)



