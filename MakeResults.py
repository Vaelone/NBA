import pandas as pd
from bs4 import BeautifulSoup
# from playwright.sync_api import sync_playwright,TimeoutError as PlaywrightTimeout
import time
import requests
from datetime import datetime
import urllib
import numpy as np

odds = pd.read_csv('rawodds.csv')
Scores = pd.read_csv('AllScores.csv')
Players23 = pd.read_csv('Players23.csv')
Players22 = pd.read_csv('Players22.csv')
Scores22 = pd.read_csv('S22NotGreat.csv')
odds['scoresMatch'] = pd.Series(dtype='int') #amount of box scores for matchups
odds['hitsMatch'] = pd.Series(dtype='int')#amount of box scores hit in matchups
odds['scores10'] = pd.Series(dtype='int')#amount of box scores pulled from last 10
odds['scores'] = pd.Series(dtype='int')#amount of box scores hit from last 10
odds['Home'] = pd.Series(dtype='bool')#True if home, false if away
Scores.loc[:, 'PLAYER_NAME'] = Scores['PLAYER_NAME'].apply(lambda x: ' '.join(x.split()[:2]))
Players23.loc[:, 'PLAYER'] = Players23['PLAYER'].apply(lambda x: ' '.join(x.split()[:2]))
#We were running into Jr. and II problems so this makes it so that everyone's only got 2 names
Scores.loc[:, 'PLAYER_NAME'] = Scores['PLAYER_NAME'].str.lower()
Players23.loc[:, 'PLAYER'] = Players23['PLAYER'].str.lower()
players_to_remove = ['bismack biyombo', 'cole anthony', 'kenrich williams', 'aleksandar vezenkov']  # Add the names of players you want to remove to this list
odds = odds[~odds['participant_name'].isin(players_to_remove)]
checkcount = 0
for index, row in odds.iterrows():
    TempScores = Scores[Scores['GAME_DATE'] < row['game_date']]
    PlayerScores = TempScores[TempScores['PLAYER_NAME'] == row['participant_name']] 
    hitcountLT=0
    totalcountLT=0
    hitcountM=0
    totalcountM=0
    PlayerScores = PlayerScores.sort_values(by = 'GAME_DATE', ascending=False)
    name = row['participant_name']
    condition = Players23['PLAYER'] == name
    # Return the value of Column1 where Column2 > 30
    if not Players23.loc[condition].empty:
    # If there are matching rows, get the 'TEAM' value from the first row
        team = Players23.loc[condition, 'TEAM'].iloc[0]
    # Continue with the rest of your code that uses the 'team' variable
    else:
        print(name)
    if team == row['AwayTeam']:
        odds.at[index, 'Home'] = False
    else:
        odds.at[index, 'Home'] = True
    for index2, row2 in PlayerScores.head(10).iterrows():
        if(row['name'] == "Over"):
            if(row2[row['description']] > row['handicap']):
                hitcountLT+=1
            totalcountLT+=1
        else:
            if(row2[row['description']] < row['handicap']):
                hitcountLT+=1
            totalcountLT+=1
    odds.at[index, 'scores10'] = totalcountLT
    odds.at[index, 'scores'] = hitcountLT
    home_team = str(row['HomeTeam'])
    away_team = str(row['AwayTeam'])
    HomeVAway = PlayerScores[PlayerScores['MATCHUP'] == (home_team + ' vs. ' + away_team)]
    HomeAAway = PlayerScores[PlayerScores['MATCHUP'] == (home_team + ' @ ' + away_team)]
    AwayVHome = PlayerScores[PlayerScores['MATCHUP'] == (away_team + ' vs. ' + home_team)]
    AwayAHome = PlayerScores[PlayerScores['MATCHUP'] == (away_team + ' @ ' + home_team)]
    AllScores = pd.concat([HomeVAway, HomeAAway, AwayVHome, AwayAHome], ignore_index=True)
    #all scores contains every box score we have of this player against this team
    FinalResults1 = AllScores[AllScores['TEAM'] == row['HomeTeam']]
    FinalResults = AllScores[AllScores['TEAM'] == row['AwayTeam']]
    #This will weed out any data of a player playing their former team
    for index3,row3 in AllScores.iterrows():
        if(row['name'] == "Over"):
            if(row3[row['description']] > row['handicap']):
                hitcountM+=1
            totalcountM+=1
        else:
            if(row3[row['description']] < row['handicap']):
                hitcountM+=1
            totalcountM+=1
    odds.at[index, 'hitsMatch'] = hitcountM
    odds.at[index, 'scoresMatch'] = totalcountM
    checkcount+=1
    if checkcount % 1000 == 0:
        print(str(checkcount) + " results created")
        
odds.to_csv('results.csv', index=False)
#Some error somewhere in this code
