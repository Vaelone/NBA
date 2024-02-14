import pandas as pd
from bs4 import BeautifulSoup
# from playwright.sync_api import sync_playwright,TimeoutError as PlaywrightTimeout
import time
import requests
from datetime import datetime
import urllib
import numpy as np

urlTeamAdvanced = 'https://stats.nba.com/stats/leaguedashteamstats?Conference=&DateFrom=&DateTo=&Division=&GameScope=&GameSegment=&Height=&ISTRound=&LastNGames=0&LeagueID=00&Location=&MeasureType=Defense&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season=2023-24&SeasonSegment=&SeasonType=Regular%20Season&ShotClockRange=&StarterBench=&TeamID=0&TwoWay=0&VsConference=&VsDivision='
urlPlayersAdvanced = 'https://stats.nba.com/stats/leaguedashplayerstats?College=&Conference=&Country=&DateFrom=&DateTo=&Division=&DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&ISTRound=&LastNGames=0&LeagueID=00&Location=&MeasureType=Misc&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season=2023-24&SeasonSegment=&SeasonType=Regular%20Season&ShotClockRange=&StarterBench=&TeamID=0&VsConference=&VsDivision=&Weight='
urlTeamsOpp = 'https://stats.nba.com/stats/leaguedashteamstats?Conference=&DateFrom=&DateTo=&Division=&GameScope=&GameSegment=&Height=&ISTRound=&LastNGames=0&LeagueID=00&Location=&MeasureType=Opponent&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season=2023-24&SeasonSegment=&SeasonType=Regular%20Season&ShotClockRange=&StarterBench=&TeamID=0&TwoWay=0&VsConference=&VsDivision='

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

responseAdvTeam = requests.get(url=urlTeamAdvanced, headers = headers).json()
responseAdvPlay = requests.get(url=urlPlayersAdvanced, headers = headers).json()
responseTeamsOpp = requests.get(url=urlTeamsOpp,headers=headers).json()
AdvTeam = responseAdvTeam['resultSets'][0]['rowSet']
AdvPlayers = responseAdvPlay['resultSets'][0]['rowSet']
TeamsOpp = responseTeamsOpp['resultSets'][0]['rowSet']

column_players = [
    "PLAYER_ID", "PLAYER_NAME", "NICKNAME", "TEAM_ID", "TEAM_ABBREVIATION",
    "AGE", "GP", "W", "L", "W_PCT", "MIN", "PTS_OFF_TOV", "PTS_2ND_CHANCE",
    "PTS_FB", "PTS_PAINT", "OPP_PTS_OFF_TOV", "OPP_PTS_2ND_CHANCE", "OPP_PTS_FB",
    "OPP_PTS_PAINT", "BLK", "BLKA", "PF", "PFD", "NBA_FANTASY_PTS", "GP_RANK",
    "W_RANK", "L_RANK", "W_PCT_RANK", "MIN_RANK", "PTS_OFF_TOV_RANK",
    "PTS_2ND_CHANCE_RANK", "PTS_FB_RANK", "PTS_PAINT_RANK", "OPP_PTS_OFF_TOV_RANK",
    "OPP_PTS_2ND_CHANCE_RANK", "OPP_PTS_FB_RANK", "OPP_PTS_PAINT_RANK", "BLK_RANK",
    "BLKA_RANK", "PF_RANK", "PFD_RANK", "NBA_FANTASY_PTS_RANK"
]

columns_team = [
    "TEAM_ID", "TEAM_NAME", "GP", "W", "L", "W_PCT", "MIN", "DEF_RATING",
    "DREB", "DREB_PCT", "STL", "BLK", "OPP_PTS_OFF_TOV", "OPP_PTS_2ND_CHANCE",
    "OPP_PTS_FB", "OPP_PTS_PAINT", "GP_RANK", "W_RANK", "L_RANK", "W_PCT_RANK",
    "MIN_RANK", "DEF_RATING_RANK", "DREB_RANK", "DREB_PCT_RANK", "STL_RANK",
    "BLK_RANK", "OPP_PTS_OFF_TOV_RANK", "OPP_PTS_2ND_CHANCE_RANK",
    "OPP_PTS_FB_RANK", "OPP_PTS_PAINT_RANK"
]
team_columns_opp = [
    "TEAM_ID", "TEAM_NAME", "GP", "W", "L", "W_PCT", "MIN", "OPP_FGM", "OPP_FGA", 
    "OPP_FG_PCT", "OPP_FG3M", "OPP_FG3A", "OPP_FG3_PCT", "OPP_FTM", "OPP_FTA", 
    "OPP_FT_PCT", "OPP_OREB", "OPP_DREB", "OPP_REB", "OPP_AST", "OPP_TOV", "OPP_STL", 
    "OPP_BLK", "OPP_BLKA", "OPP_PF", "OPP_PFD", "OPP_PTS", "PLUS_MINUS", "GP_RANK", 
    "W_RANK", "L_RANK", "W_PCT_RANK", "MIN_RANK", "OPP_FGM_RANK", "OPP_FGA_RANK", 
    "OPP_FG_PCT_RANK", "OPP_FG3M_RANK", "OPP_FG3A_RANK", "OPP_FG3_PCT_RANK", 
    "OPP_FTM_RANK", "OPP_FTA_RANK", "OPP_FT_PCT_RANK", "OPP_OREB_RANK", "OPP_DREB_RANK", 
    "OPP_REB_RANK", "OPP_AST_RANK", "OPP_TOV_RANK", "OPP_STL_RANK", "OPP_BLK_RANK", 
    "OPP_BLKA_RANK", "OPP_PF_RANK", "OPP_PFD_RANK", "OPP_PTS_RANK", "PLUS_MINUS_RANK"
]

AdvTeamDf = pd.DataFrame(AdvTeam, columns = columns_team)
AdvPlayersDf = pd.DataFrame(AdvPlayers, columns = column_players)
TeamOppDf = pd.DataFrame(TeamsOpp, columns = team_columns_opp)
selectedColumnsP = ["PLAYER_NAME", "TEAM_ABBREVIATION", "GP", "PTS_OFF_TOV", "PTS_2ND_CHANCE", 'PTS_FB', 'PTS_PAINT' ]
selectedColumnsT = ['TEAM_NAME', 'OPP_PTS_OFF_TOV', 'OPP_PTS_2ND_CHANCE', 'OPP_PTS_FB', 'OPP_PTS_PAINT' ]
selectedColumnsTOpp = ['TEAM_NAME', "OPP_FG3M", "OPP_FTM", "OPP_REB", "OPP_AST", "OPP_TOV", "OPP_STL","OPP_BLK","OPP_PTS","OPP_FG3M_RANK",
    "OPP_REB_RANK", "OPP_AST_RANK", "OPP_TOV_RANK", "OPP_STL_RANK", "OPP_BLK_RANK", "OPP_PTS_RANK"]

AdvTeamFilt= AdvTeamDf[selectedColumnsT]
AdvPlayersFilt = AdvPlayersDf[selectedColumnsP]
TeamOppFilt = TeamOppDf[selectedColumnsTOpp]
Players23 = pd.read_csv('Players23.csv')
Players23['PPG'] = Players23['PTS']/Players23['GP']
Players23Filt = Players23[Players23['PPG'] >= 8.5]
 # Merge the two DataFrames on the 'PLAYER' and 'PLAYER_NAME' columns
print(AdvPlayersFilt)
print(Players23Filt)
AdvPlayersFilt['PLAYER_NAME'] = AdvPlayersFilt['PLAYER_NAME'].apply(lambda x: ' '.join(x.split()[:2]))
AdvPlayersFilt.loc[:, 'PLAYER_NAME'] = AdvPlayersFilt['PLAYER_NAME'].str.lower()
merged_df = pd.merge(AdvPlayersFilt, Players23Filt, left_on='PLAYER_NAME', right_on='PLAYER', how='left')
# Drop the duplicate 'PLAYER' column (if needed)
Players23Adv = merged_df.drop(columns=['PLAYER'])
print(Players23Adv)

# Now add 'PTS' directly from 'Players23Filt'
Players23Adv['PTS_OFF_TOV_PCT'] = Players23Adv['PTS_OFF_TOV'] / Players23Adv['PPG']
Players23Adv['PTS_2ND_PCT'] = Players23Adv['PTS_2ND_CHANCE'] / Players23Adv['PPG']
Players23Adv['PTS_PAINT_PCT'] = Players23Adv['PTS_PAINT'] / Players23Adv['PPG']
Players23Adv['PTS_FB_PCT'] = Players23Adv['PTS_FB'] / Players23Adv['PPG']

TovScorers = Players23Adv.nlargest(10, 'PTS_OFF_TOV_PCT')
TovScorers.to_csv('TovScorers.csv', index=False)
SecondScorers = Players23Adv.nlargest(10, 'PTS_OFF_TOV_PCT')
SecondScorers.to_csv('SecondScorers.csv', index=False)
FBScorers = Players23Adv.nlargest(10, 'PTS_OFF_TOV_PCT')
FBScorers.to_csv('FBScorers.csv', index=False) 
PaintScorers = Players23Adv.nlargest(10, 'PTS_OFF_TOV_PCT')
PaintScorers.to_csv('PaintScorers.csv', index=False)
merged_df2 = pd.merge(AdvTeamFilt, TeamOppFilt, on='TEAM_NAME', how='inner')

# Drop the duplicate 'PLAYER' column (if needed)
Teams23Adv = merged_df2
Teams23Adv['OPP_PTS_OFF_TOV_PCT'] = Teams23Adv['OPP_PTS_OFF_TOV'] / Teams23Adv['OPP_PTS']
Teams23Adv['OPP_PTS_2ND_PCT'] = Teams23Adv['OPP_PTS_2ND_CHANCE'] / Teams23Adv['OPP_PTS']
Teams23Adv['OPP_PTS_PAINT_PCT'] = Teams23Adv['OPP_PTS_PAINT'] / Teams23Adv['OPP_PTS']
Teams23Adv['OPP_PTS_FB_PCT'] = Teams23Adv['OPP_PTS_FB'] / Teams23Adv['OPP_PTS']
StrongTovTeams = Teams23Adv.nsmallest(5, 'OPP_PTS_OFF_TOV_PCT')[['OPP_PTS_OFF_TOV_PCT', 'TEAM_NAME']]
StrongSecondTeams = Teams23Adv.nsmallest(5, 'OPP_PTS_2ND_PCT')[['OPP_PTS_2ND_PCT', 'TEAM_NAME']]
StrongFBTeams = Teams23Adv.nsmallest(5, 'OPP_PTS_FB_PCT')[['OPP_PTS_FB_PCT', 'TEAM_NAME']]
StrongPaintTeams = Teams23Adv.nsmallest(5, 'OPP_PTS_PAINT_PCT')[['OPP_PTS_PAINT_PCT', 'TEAM_NAME']] 
team_abbreviations = {
            'Atlanta Hawks': 'ATL',
            'Boston Celtics': 'BOS',
            'Brooklyn Nets': 'BKN',
            'Charlotte Hornets': 'CHA',
            'Chicago Bulls': 'CHI',
            'Cleveland Cavaliers': 'CLE',
            'Dallas Mavericks': 'DAL',
            'Denver Nuggets': 'DEN',
            'Detroit Pistons': 'DET',
            'Golden State Warriors': 'GSW',
            'Houston Rockets': 'HOU',
            'Indiana Pacers': 'IND',
            'LA Clippers': 'LAC',
            'Los Angeles Lakers': 'LAL',
            'Memphis Grizzlies': 'MEM',
            'Miami Heat': 'MIA',
            'Milwaukee Bucks': 'MIL',
            'Minnesota Timberwolves': 'MIN',
            'New Orleans Pelicans': 'NOP',
            'New York Knicks': 'NYK',
            'Oklahoma City Thunder': 'OKC',
            'Orlando Magic': 'ORL',
            'Philadelphia 76ers': 'PHI',
            'Phoenix Suns': 'PHX',
            'Portland Trail Blazers': 'POR',
            'Sacramento Kings': 'SAC',
            'San Antonio Spurs': 'SAS',
            'Toronto Raptors': 'TOR',
            'Utah Jazz': 'UTA',
            'Washington Wizards': 'WAS',
        }
WeakTovTeams = Teams23Adv.nlargest(5, 'OPP_PTS_OFF_TOV_PCT')[['OPP_PTS_OFF_TOV_PCT', 'TEAM_NAME']]
WeakTovTeams['TEAM_NAME'] = WeakTovTeams['TEAM_NAME'].map(team_abbreviations)
WeakTovTeams.to_csv('WeakTovTeams.csv', index=False)
WeakSecondTeams = Teams23Adv.nlargest(5, 'OPP_PTS_2ND_PCT')[['OPP_PTS_2ND_PCT', 'TEAM_NAME']]
WeakSecondTeams['TEAM_NAME'] = WeakSecondTeams['TEAM_NAME'].map(team_abbreviations)
WeakSecondTeams.to_csv('WeakSecondTeams.csv', index=False)
WeakFBTeams = Teams23Adv.nlargest(5, 'OPP_PTS_FB_PCT')[['OPP_PTS_FB_PCT', 'TEAM_NAME']]
WeakFBTeams['TEAM_NAME'] = WeakFBTeams['TEAM_NAME'].map(team_abbreviations)
WeakFBTeams.to_csv('WeakFBTeams.csv', index=False)
WeakPaintTeams = Teams23Adv.nlargest(5, 'OPP_PTS_PAINT_PCT')[['OPP_PTS_PAINT_PCT', 'TEAM_NAME']]
WeakPaintTeams['TEAM_NAME'] = WeakPaintTeams['TEAM_NAME'].map(team_abbreviations) 
WeakPaintTeams.to_csv('WeakPaintTeams.csv', index=False)

#Make sure we only use for overs or unders