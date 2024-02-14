import pandas as pd
from bs4 import BeautifulSoup
# from playwright.sync_api import sync_playwright,TimeoutError as PlaywrightTimeout
import time
import requests
from datetime import datetime
import urllib
import numpy as np


urlPlayers23 = 'https://stats.nba.com/stats/leagueLeaders?LeagueID=00&PerMode=Totals&Scope=S&Season=2023-24&SeasonType=Regular%20Season&StatCategory=MIN'

urlPlayers22 = 'https://stats.nba.com/stats/leagueLeaders?LeagueID=00&PerMode=Totals&Scope=S&Season=2022-23&SeasonType=Regular%20Season&StatCategory=MIN'

urlScores23 = 'https://stats.nba.com/stats/leaguegamelog?Counter=1000&DateFrom=&DateTo=&Direction=DESC&ISTRound=&LeagueID=00&PlayerOrTeam=P&Season=2023-24&SeasonType=Regular%20Season&Sorter=DATE'

urlScores22 = 'https://stats.nba.com/stats/leaguegamelog?Counter=1000&DateFrom=&DateTo=&Direction=DESC&ISTRound=&LeagueID=00&PlayerOrTeam=P&Season=2022-23&SeasonType=Regular%20Season&Sorter=DATE'
#Players contains the season long averages for players, appears to be cutoff at 10 minutes per game
#Scores contains the box scores for every game every player in the league

headers  = {
    'Host': 'stats.nba.com',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'Accept': 'application/json, text/plain, */*',
    'x-nba-stats-token': 'true',
    'X-NewRelic-ID': 'VQECWF5UChAHUlNTBwgBVw==',
    'DNT': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
    'x-nba-stats-origin': 'stats',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Referer': 'https://stats.nba.com/',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
}
#acquired from the internet, and required to scrape nba.com

responsePlayers23 = requests.get(url=urlPlayers23, headers = headers).json()
responsePlayers22 = requests.get(url=urlPlayers22, headers = headers).json()
responseScores23 = requests.get(url=urlScores23,headers = headers).json()
responseScores22 = requests.get(url=urlScores22,headers = headers).json()
#Using the requests library and the api url to get a response

players23 = responsePlayers23['resultSet']['rowSet']
players22 = responsePlayers22['resultSet']['rowSet']
scores23 = responseScores23['resultSets'][0]['rowSet']
scores22 = responseScores22['resultSets'][0]['rowSet']
#resultSet and rowset are both found in teh html from webscraping

columns_list_players = [
"PLAYER_ID",
"RANK",
"PLAYER",
"TEAM_ID",
"TEAM",
"GP",
"MIN",
"FGM",
"FGA",
"FG_PCT",
"FG3M",
"FG3A",
"FG3_PCT",
"FTM",
"FTA",
"FT_PCT",
"OREB",
"DREB",
"REB",
"AST",
"STL",
"BLK",
"TOV",
"PF",
"PTS",
"EFF",
"AST_TOV",
"STL_TOV"
]

columns_list_scores = [ 
"SEASON_ID",
"PLAYER_ID",
"PLAYER_NAME",
"TEAM_ID",
"TEAM_ABBREVIATION",
"TEAM_NAME",
"GAME_ID",
"GAME_DATE",
"MATCHUP",
"WL",
"MIN",
"FGM",
"FGA",
"FG_PCT",
"FG3M",
"FG3A",
"FG3_PCT",
"FTM",
"FTA",
"FT_PCT",
"OREB",
"DREB",
"REB",
"AST",
"STL",
"BLK",
"TOV",
"PF",
"PTS",
"PLUS_MINUS",
"FANTASY_PTS",
"VIDEO_AVAILABLE"
]

Players2023_df = pd.DataFrame(players23, columns = columns_list_players)
Players2022_df = pd.DataFrame(players22, columns = columns_list_players)
Scores2023_df = pd.DataFrame(scores23, columns = columns_list_scores)
Scores2022_df = pd.DataFrame(scores22, columns = columns_list_scores)
#All aforementioned data organized into pandas dataframes

FilteredScores23 = pd.merge(Scores2023_df, Players2023_df, 
                                        on='PLAYER_ID', how='inner', suffixes=('_Scores', '_Players'))
FilteredScores22 = pd.merge(Scores2022_df, Players2023_df, 
                                        on='PLAYER_ID', how='inner', suffixes=('_Scores', '_Players'))
#We use players2023 for both 2022 and 2023, because the only terms for which we are using the 2022 DF 
#is to create predictions based on their 2023 team. If they moved we do not want them
#Merging the Scores and players dataframes for each year
selected_columns = [col for col in FilteredScores23.columns if '_Scores' in col]
other_columns = ['SEASON_ID','PLAYER_ID', 'PLAYER_NAME','TEAM','GAME_DATE','GAME_ID','MATCHUP']
selected_columns = other_columns + selected_columns
#Selecting only the columns that came from the scores dataframe
#Had to manually add these others, because they were not duplicated in the merge
FilteredScores23 = FilteredScores23[selected_columns]
FilteredScores22 = FilteredScores22[selected_columns]
#Filtering our merged set to only contain the scores columns
FilteredScores23.columns = FilteredScores23.columns.str.replace('_Scores', '')
FilteredScores22.columns = FilteredScores22.columns.str.replace('_Scores', '')
#Removing the scores suffix we added in line 118
Scores = pd.concat([FilteredScores22,FilteredScores23], ignore_index=True)
Players = Players2023_df
#To this point we have Scores, a pandas dataframe containing every box score of every relevant player
#We also have Player, which contains all the aforementioned relevant players from this year
#We finally have odds, which contains every player, and their odds for every stat according to barstool
#We need to rename the columns in scores to match the format of data.csv. This is easier than
#the other way around, because we 
#WE HAVE TO RENAME THE DESCRIPTION COLUMN TO REMOVE THE PLAYER'S NAME
Scores['Total Points, Rebounds And Assists'] = Scores['PTS'] + Scores['REB'] + Scores['AST']
Scores['Total Points And Rebounds'] = Scores['PTS'] + Scores['REB']
Scores['Total Points And Assists'] = Scores['PTS'] + Scores['AST']
Scores['Total Assists And Rebounds'] = Scores['AST'] + Scores['REB']
Scores['Total Steals And Blocks'] = Scores['STL'] + Scores['BLK']
renamedColumns = {
    'PTS': 'Total Points',
    'REB': 'Total Rebounds',
    'AST': 'Total Assists',
    'BLK': 'Total Blocks',
    'STL' : 'Total Steals' ,
    'FG3M': 'Total Threes Made',
    'TOV': 'Total Turnovers'
}
Scores.rename(columns=renamedColumns, inplace=True)
Scores.loc[:,'PLAYER_NAME'] = Scores['PLAYER_NAME'].apply(lambda x: ' '.join(x.split()[:2]))
Players.loc[:, 'PLAYER'] = Players['PLAYER'].apply(lambda x: ' '.join(x.split()[:2]))
Players2022_df.loc[:, 'PLAYER'] = Players2022_df['PLAYER'].apply(lambda x: ' '.join(x.split()[:2]))
FilteredScores22['PLAYER_NAME'] = FilteredScores22['PLAYER_NAME'].apply(lambda x: ' '.join(x.split()[:2]))
Scores.loc[:, 'PLAYER_NAME'] = Scores['PLAYER_NAME'].str.lower()
Players2022_df.loc[:, 'PLAYER'] = Players2022_df['PLAYER'].str.lower()
Players.loc[:, 'PLAYER'] = Players['PLAYER'].str.lower()
FilteredScores22['PLAYER_NAME'] = FilteredScores22['PLAYER_NAME'].str.lower()
Scores.to_csv('AllScores.csv', index=False)
Players.to_csv('Players23.csv', index=False)
Players2022_df.to_csv('Players22.csv', index=False)
FilteredScores22.to_csv('S22NotGreat.csv', index=False)










