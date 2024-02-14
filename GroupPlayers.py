import pandas as pd
from bs4 import BeautifulSoup
# from playwright.sync_api import sync_playwright,TimeoutError as PlaywrightTimeout
import time
import requests
from datetime import datetime
import urllib
import numpy as np

#Future ideas
    #Group on defense vs position
    #Look at moneyline
    #Opp Pts Paint
    #Opp Pts off TOV
    #Opp Pts off


Players22 = pd.read_csv('Players22.csv')
Players23 = pd.read_csv('Players23.csv')

teams = ['ATL', 'BOS', 'BKN', 'CHA', 'CHI', 'CLE', 'DAL', 'DEN', 'DET', 'GSW', 'HOU', 'IND',
          'LAC', 'LAL', 'MEM', 'MIA', 'MIL', 'MIN', 'NOP', 'NYK', 'OKC', 'ORL', 'PHI', 'PHX', 
          'POR', 'SAC', 'SAS', 'TOR', 'UTA', 'WAS']

SamePlayersNewRoles = []
NewPlayersPlaying= []

for team in teams:
    Roster23 = Players23[Players23['TEAM'] == team]
    Roster22 = Players22[Players22['TEAM'] == team]
    NewPlayers = Roster23[~Roster23['PLAYER'].isin(Roster22['PLAYER'])]
    SamePlayers23 = Roster23[Roster23['PLAYER'].isin(Roster22['PLAYER'])]
    SamePlayers22 = Roster22[Roster22['PLAYER'].isin(Roster22['PLAYER'])]
    mpg23 = Roster23['MIN'].sum() / Roster23['GP'].sum()
    mpg22 = Roster22['MIN'].sum() / Roster22['GP'].sum()
    newplayersmpg = NewPlayers['MIN'].sum() / NewPlayers['GP'].sum()
    sameplayers23mpg = SamePlayers23['MIN'].sum() / SamePlayers23['GP'].sum()
    sameplayers22mpg = SamePlayers22['MIN'].sum() / SamePlayers22['GP'].sum()
    if(sameplayers23mpg > sameplayers22mpg*1.15):
        SamePlayersNewRoles.append(team)
    #We use this if because even if they are the same players, it is relevant if they have much larger roles
    if(sameplayers23mpg < newplayersmpg*1.13):
        NewPlayersPlaying.append(team)
    #We use this to check if newPlayers are having a large amount of playing time
print('SamePlayersNewRoles')
print(SamePlayersNewRoles)
print('NewPlayersPlaying')
print(NewPlayersPlaying)
testTeams = list(set(SamePlayersNewRoles + NewPlayersPlaying))
df = pd.DataFrame(testTeams, columns=['Team'])
df.to_csv('testTeams.csv', index = False)



