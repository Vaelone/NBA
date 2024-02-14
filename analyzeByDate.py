import pandas as pd
from bs4 import BeautifulSoup
# from playwright.sync_api import sync_playwright,TimeoutError as PlaywrightTimeout
import time
import requests
from datetime import datetime
import urllib
import numpy as np
import sys 
from datetime import timedelta
#Find out how to round to 2 decimal places
#Somewhere down the line - Make a web app that allows the user to see whatever correlation they want
#MUST DO - READ THROUGH THE ENTIRE THING AND MAKE SURE THERE IS NO UNNECESARRY WEBSCRAPING CODE,
#WE ALSO MUST TAKE THE DATE TIME INTO ACCOUNT, DO NOT FORGET TO DO THAT AS WELL.
results = pd.read_csv('results.csv')
#1132 - 10.5,76.92307692307693,derrick jones,Under,Total Points And Rebounds,DAL,SAS,2023-10-25,0.0,0.0,10.0,6.0,False
#1133 - 20.5,86.95652173913044,devin vassell,Under,Total Points And Rebounds,DAL,SAS,2023-10-25,0.0,0.0,10.0,8.0,True
#4156 - 4.5,95.23809523809524,norman powell,Over,Total Assists And Rebounds,POR,LAC,2023-10-25,2.0,2.0,10.0,4.0,True
#4157 - 9.5,105.0,paul george,Over,Total Assists And Rebounds,POR,LAC,2023-10-25,1.0,1.0,10.0,6.0,True
Scores = pd.read_csv('AllScores.csv')
results['Hits'] = False
hitcount=0
misscount=0
totaltencount = 0
homeodds = 0
homecount = 0
homehits = 0
awayodds = 0
awaycount = 0
awayhits = 0
matchodds = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,0.0]
matchfilterodds = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,0.0]
matchhitfiltercounts = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,0.0]
matchfiltercounts = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,0.0]
MatchupTeams = pd.read_csv('testTeams.csv')
matchhitcounts = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,0.0]
matchcounts = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,0.0]
tenodds = [0.0] * 11
hitcounts = [0.0] * 11
tencounts = [0.0] * 11
results['scores'] = results['scores'].astype(int)
results['scores10'] = results['scores10'].astype(int)
Scores['PLAYER_NAME'] = Scores['PLAYER_NAME'].apply(lambda x: ' '.join(x.split()[:2]))
#Get rid of all the possible Jr. II suffixes
FBScorers = pd.read_csv('FBScorers.csv')
PaintScorers = pd.read_csv('PaintScorers.csv')
SecondScorers = pd.read_csv('SecondScorers.csv')
TovScorers = pd.read_csv('TovScorers.csv')
WeakFBTeamsRaw = pd.read_csv('WeakFBTeams.csv')
WeakPaintTeamsRaw = pd.read_csv('WeakPaintTeams.csv')
WeakSecondTeamsRaw = pd.read_csv('WeakSecondTeams.csv')
WeakTovTeamsRaw = pd.read_csv('WeakTovTeams.csv')
FBScorers['PLAYER_NAME'] = FBScorers['PLAYER_NAME'].apply(lambda x: ' '.join(x.split()[:2]))
FBScorers['PLAYER_NAME'] = FBScorers['PLAYER_NAME'].str.lower()
FBPlayers = FBScorers['PLAYER_NAME'].unique()
FBPlayers = FBPlayers.astype(str)
#We can filter this more if we need to
PaintScorers['PLAYER_NAME'] = PaintScorers['PLAYER_NAME'].apply(lambda x: ' '.join(x.split()[:2]))
PaintScorers['PLAYER_NAME'] = PaintScorers['PLAYER_NAME'].str.lower()
PaintPlayers = PaintScorers['PLAYER_NAME'].unique()
PaintPlayers = PaintPlayers.astype(str)
#We can filter this more if we need to
SecondScorers['PLAYER_NAME'] = SecondScorers['PLAYER_NAME'].apply(lambda x: ' '.join(x.split()[:2]))
SecondScorers['PLAYER_NAME'] = SecondScorers['PLAYER_NAME'].str.lower()
SecondPlayers = SecondScorers['PLAYER_NAME'].unique()
SecondPlayers = SecondPlayers.astype(str)
#We can filter this more if we need to
TovScorers['PLAYER_NAME'] = TovScorers['PLAYER_NAME'].apply(lambda x: ' '.join(x.split()[:2]))
TovScorers['PLAYER_NAME'] = TovScorers['PLAYER_NAME'].str.lower()
TovPlayers = TovScorers['PLAYER_NAME'].unique()
TovPlayers = TovPlayers.astype(str)
WeakFBTeamss = WeakFBTeamsRaw['TEAM_NAME']
WeakPaintTeamss = WeakPaintTeamsRaw['TEAM_NAME']
WeakSecondTeamss = WeakSecondTeamsRaw['TEAM_NAME']
WeakTovTeamss = WeakTovTeamsRaw['TEAM_NAME']
WeakFBTeams = WeakFBTeamss.astype(str)
WeakPaintTeams = WeakPaintTeamss.astype(str)
WeakSecondTeams = WeakSecondTeamss.astype(str)
WeakTovTeams = WeakTovTeamss.astype(str)
#We can filter this more if we need to
FBoddsO = 0
TovoddsO = 0
SecondoddsO = 0
PaintoddsO = 0
FBoddsU = 0
TovoddsU = 0
SecondoddsU = 0
PaintoddsU = 0
FBHitsO = 0
FBTotalO = 0
FBHitsU = 0
FBTotalU = 0
TovHitsO = 0
TovTotalO = 0
TovHitsU = 0
TovTotalU = 0
SecondHitsO = 0
SecondTotalO = 0
SecondHitsU = 0
SecondTotalU = 0
PaintHitsO = 0
PaintTotalO = 0
PaintHitsU = 0
PaintTotalU = 0
Scores['GAME_DATE'] = pd.to_datetime(Scores['GAME_DATE'])
results['game_date'] = pd.to_datetime(results['game_date'])
analyzecount = 0
date = datetime(2024,1,10)
resultsNew = results[results['game_date'] > date]
for index,row in resultsNew.iterrows():
    TempScores = Scores[(Scores['GAME_DATE'] == row['game_date'])]
    awayTeam = row['AwayTeam']
    homeTeam = row['HomeTeam']
    ou = row['name']
    name = row['participant_name']
    name = ' '.join(name.split()[:2])
    name = name.lower()
    #Makes each name only two words
    line = row['handicap']
    stat = row['description']
    #Get rid of all the Jrs.
    PlayerRow = TempScores[TempScores['PLAYER_NAME'].str.lower() == name.lower()]
    if not PlayerRow.empty:
        Team1 = PlayerRow['TEAM'].iloc[0]
    else:
        # Handle empty DataFrame case - occurs when the player has odds but does not every end up playing
        print(name)
        continue
    Team1 = str(Team1)
    matchup = ''
    if Team1 == awayTeam:
        matchup = homeTeam
    else:
        matchup = awayTeam
    #Anybody who switched teams will not be considred in this
    #Any rookies shouldn't be calculated
    if(ou == 'Under'):
        if(PlayerRow.iloc[0][stat] < line):
            results.at[index, 'Hits'] = True
            if(row['Home']):
                homecount+=1
                homehits+=1
                homeodds += row['odds']
            else:
                awaycount+=1
                awayhits+=1
                awayodds += row['odds']
            if matchup in WeakFBTeams.values:
                if name in FBPlayers:
                    FBHitsU+=1
                    FBTotalU+=1
                    FBoddsU += row['odds']
            if matchup in WeakTovTeams.values:
                if name in TovPlayers:
                    TovHitsU+=1
                    TovTotalU+=1
                    TovoddsU += row['odds']
            if matchup in WeakSecondTeams.values:
                if name in SecondPlayers:
                    SecondHitsU+=1
                    SecondTotalU+=1
                    SecondoddsU += row['odds']
            if matchup in WeakPaintTeams.values:
                if name in PaintPlayers:
                    PaintHitsU+=1
                    PaintTotalU+=1
                    PaintoddsU += row['odds']
            if(results.at[index,'scoresMatch'] > 3):
                indexPCT = (results.at[index, 'hitsMatch'] / results.at[index, 'scoresMatch']) * 100
                #here we calculate the percent of prior box scores that hit, and multiply by 100
                index = int(indexPCT)//12.5
                index = int(index)
                matchhitcounts[index] += 1
                matchcounts[index] +=1
                matchodds[index] += row['odds']
                if matchup not in MatchupTeams['Team'].values:
                    matchhitfiltercounts[index] += 1
                    matchfiltercounts[index] +=1
                    matchfilterodds[index] += row['odds']
            if(results.at[index, 'scores10'] == 10):
                hitcounts[int(results.at[index, 'scores'])] += 1
                tencounts[int(results.at[index, 'scores'])] += 1
                tenodds[int(results.at[index, 'scores'])] += row['odds']
                #This will add one onto the proper value in the list
            hitcount+=1
        else:
            if(row['Home']):
                homecount+=1
            else:
                awaycount+=1
            if matchup in WeakFBTeams.values:
                if name in FBPlayers:
                    FBTotalU+=1
            if matchup in WeakTovTeams.values:
                if name in TovPlayers:
                    TovTotalU+=1
            if matchup in WeakSecondTeams.values:
                if name in SecondPlayers:
                    SecondTotalU+=1
            if matchup in WeakPaintTeams.values:
                if name in PaintPlayers:
                    PaintTotalU+=1
            if(results.at[index, 'scoresMatch'] > 3):
                indexPCT = (results.at[index, 'hitsMatch'] / results.at[index, 'scoresMatch']) * 100
                #here we calculate the percent of prior box scores that hit, and multiply by 100
                index = int(indexPCT)//12.5
                index = int(index)
                matchcounts[index] +=1
                if matchup not in MatchupTeams['Team'].values:
                    matchfiltercounts[index] += 1
            if(results.at[index, 'scores10'] == 10):
                tencounts[int(results.at[index, 'scores'])] += 1
            results.at[index, 'Hits'] = False
            misscount+=1
    else:
        if(PlayerRow.iloc[0][stat] > line):
            results.at[index, 'Hits'] = True
            if(row['Home']):
                homecount+=1
                homehits+=1
                homeodds += row['odds']
            else:
                awaycount+=1
                awayhits+=1
                awayodds += row['odds']
            if matchup in WeakFBTeams.values:
                if name in FBPlayers:
                    FBHitsO+=1
                    FBTotalO+=1
                    FBoddsO += row['odds']
            if matchup in WeakTovTeams.values:
                if name in TovPlayers:
                    TovHitsO+=1
                    TovTotalO+=1
                    TovoddsO += row['odds']
            if matchup in WeakSecondTeams.values:
                if name in SecondPlayers:
                    SecondHitsO+=1
                    SecondTotalO+=1
                    SecondoddsO += row['odds']
            if matchup in WeakPaintTeams.values:
                if name in PaintPlayers:
                    PaintHitsO+=1
                    PaintTotalO+=1
                    PaintoddsO += row['odds']
            if(results.at[index,'scoresMatch'] > 3):
                indexPCT = (results.at[index, 'hitsMatch'] / results.at[index, 'scoresMatch']) * 100
                #here we calculate the percent of prior box scores that hit, and multiply by 100
                index = int(indexPCT)//12.5
                index = int(index)
                matchhitcounts[index] += 1
                matchcounts[index] +=1
                matchodds[index] += row['odds']
                if matchup not in MatchupTeams['Team'].values:
                    matchhitfiltercounts[index] += 1
                    matchfiltercounts[index] +=1
                    matchfilterodds[index] += row['odds']
            if(results.at[index, 'scores10'] == 10):
                hitcounts[int(results.at[index, 'scores'])] += 1
                tencounts[int(results.at[index, 'scores'])] += 1
                tenodds[int(results.at[index, 'scores'])] += row['odds']
                #This will add one onto the proper value in the list
            hitcount+=1
        else:
            if(row['Home']):
                homecount+=1
            else:
                awaycount+=1
            if matchup in WeakFBTeams.values:
                if name in FBPlayers:
                    FBTotalO+=1
            if matchup in WeakTovTeams.values:
                if name in TovPlayers:
                    TovTotalO+=1
            if matchup in WeakSecondTeams.values:
                if name in SecondPlayers:
                    SecondTotalO+=1
            if matchup in WeakPaintTeams.values:
                if name in PaintPlayers:
                    PaintTotalO+=1
            if(results.at[index, 'scoresMatch'] > 3):
                indexPCT = (results.at[index, 'hitsMatch'] / results.at[index, 'scoresMatch']) * 100
                #here we calculate the percent of prior box scores that hit, and multiply by 100
                index = int(indexPCT)//12.5
                index = int(index)
                matchcounts[index] +=1
                if matchup not in MatchupTeams['Team'].values:
                    matchfiltercounts[index] += 1
            if(results.at[index, 'scores10'] == 10):
                tencounts[int(results.at[index, 'scores'])] += 1
            results.at[index, 'Hits'] = False
            misscount+=1
    analyzecount+=1
    if analyzecount % 1000 == 0:
        print(str(analyzecount) + " entries analyzed")
original_stdout = sys.stdout
output_file_path = 'output' + str(date) + '.txt'
with open(output_file_path, 'w') as f:
    sys.stdout = f
    for i in range(11):
        print("Hit percentage when " + str(i) + " of last 10 hit")
        print((hitcounts[i] / tencounts[i]) * 100)
        print("Total Sample Size: " + str(tencounts[i]))
        print("Average odds of hits: " + str(tenodds[i] / hitcounts[i]))
        profittotal = ((hitcounts[i] / tencounts[i]) * 100) * (1 + (tenodds[i] / hitcounts[i])/100)
        profit = profittotal - 100
        rounded_profit = round(profit, 2)
        print("You would make/lose " + str(rounded_profit) + " if you bet 100 dollars on this trend")
        print('\n')

        
    for i in range(9):
        if(i != 8):
            print("Hit percentage when " + str(i * 12.5) + "-" + str((i+1)*12.5) + " percent  of prior matchups hit")
        else:
            print("Hit percentage when " + str(i * 12.5) + " percent  of prior matchups hit")
        if(matchcounts[i] != 0):
            print((matchhitcounts[i]/matchcounts[i]) * 100)
            print("Total Sample Size: " + str(matchcounts[i]))
            print("Average odds of hits: " + str(matchodds[i] / matchhitcounts[i]))
            profittotal = ((matchhitcounts[i] / matchcounts[i]) * 100) * (1 + (matchodds[i] / matchhitcounts[i])/100)
            profit = profittotal - 100
            rounded_profit = round(profit, 2)
            print("You would make/lose " + str(rounded_profit) + " if you bet 100 dollars on this trend")
        else:
            print("Total Sample Size: " + str(matchcounts[i]))
        print('\n')
    for i in range(9):
        if(i != 8):
            print("Hit percentage when " + str(i * 12.5) + "-" + str((i+1)*12.5) + " percent  of prior matchups hit(Filtered)")
        else:
            print("Hit percentage when " + str(i * 12.5) + " percent  of prior matchups hit (Filtered)")
        if(matchfiltercounts[i] != 0):
            print((matchhitfiltercounts[i]/matchfiltercounts[i]) * 100)
            print("Total Sample Size: " + str(matchfiltercounts[i]))
            print("Average odds of hits: " + str(matchfilterodds[i] / matchhitfiltercounts[i]))
            profittotal = ((matchhitfiltercounts[i] / matchfiltercounts[i]) * 100) * (1 + (matchfilterodds[i] / matchhitfiltercounts[i])/100)
            profit = profittotal - 100
            rounded_profit = round(profit, 2)
            print("You would make/lose " + str(rounded_profit) + " if you bet 100 dollars on this trend")
        else:
            print("Total Sample Size: " + str(matchfiltercounts[i]))
        print('\n')

    print("Hit percentage when player is home: " + str((homehits/homecount) * 100))
    print("Total Sample Size: " + str(homecount))
    print("Average odds of hits: " + str(homeodds / homehits))
    profittotal = ((homehits/homecount) * 100) * (1 + (homeodds / homehits)/100)
    profit = profittotal - 100
    rounded_profit = round(profit, 2)
    print("You would make/lose " + str(rounded_profit) + " if you bet 100 dollars on this trend")
    print('\n')
    print("Hit percentage when player is away: " + str((awayhits/awaycount) * 100))
    print("Total Sample Size: " + str(awaycount))
    print("Average odds of hits: " + str(awayodds / awayhits))
    profittotal = ((awayhits/awaycount) * 100) * (1 + (awayodds / awayhits)/100)
    profit = profittotal - 100
    rounded_profit = round(profit, 2)
    print("You would make/lose " + str(rounded_profit) + " if you bet 100 dollars on this trend")
    
    print('\n')
    print("OVERS:")
    if(FBTotalO == 0):
        print('No sample size')
    else:
        print("Fast Break Scorers against Weak Fast Break Defenses: " + str((FBHitsO/FBTotalO) * 100))
        print("Total Sample Size: " + str(FBTotalO))
        print("Average odds of hits: " + str(FBoddsO / FBHitsO))
        profittotal = ((FBHitsO/FBTotalO) * 100) * (1 + (FBoddsO / FBHitsO)/100)
        profit = profittotal - 100
        rounded_profit = round(profit, 2)
        print("You would make/lose " + str(rounded_profit) + " if you bet 100 dollars on this trend")
        print('\n')
    if(TovTotalO == 0):
        print('No sample size')
    else:
        print("Turnover Scorers against Weak Turnover Defenses: " + str((TovHitsO/TovTotalO) * 100))
        print("Total Sample Size: " + str(TovTotalO))
        print("Average odds of hits: " + str(TovoddsO / TovHitsO))
        profittotal = ((TovHitsO/TovTotalO) * 100) * (1 + (TovoddsO / TovHitsO)/100)
        profit = profittotal - 100
        rounded_profit = round(profit, 2)
        print("You would make/lose " + str(rounded_profit) + " if you bet 100 dollars on this trend")
        print('\n')
    if(SecondTotalO == 0):
        print('No sample size')
    else:
        print("Second Chance Scorers against Weak Second Chance Defenses: " + str((SecondHitsO/SecondTotalO) * 100))
        print("Total Sample Size: " + str(SecondTotalO))
        print("Average odds of hits: " + str(SecondoddsO / SecondHitsO))
        profittotal = ((SecondHitsO/SecondTotalO) * 100) * (1 + (SecondoddsO / SecondHitsO)/100)
        profit = profittotal - 100
        rounded_profit = round(profit, 2)
        print("You would make/lose " + str(rounded_profit) + " if you bet 100 dollars on this trend")
        print('\n')
    if(PaintTotalO == 0):
        print('No sample size')
    else:
        print("Paint Scorers against Weak Paint Defenses: " + str((PaintHitsO/PaintTotalO) * 100))
        print("Total Sample Size: " + str(PaintTotalO))
        print("Average odds of hits: " + str(PaintoddsO / PaintHitsO))
        profittotal = ((PaintHitsO/PaintTotalO) * 100) * (1 + (PaintoddsO / PaintHitsO)/100)
        profit = profittotal - 100
        rounded_profit = round(profit, 2)
        print("You would make/lose " + str(rounded_profit) + " if you bet 100 dollars on this trend")
        print('\n')

    print("UNDERS:")
    if(FBTotalO == 0):
        print('No sample size')
    else:
        print("Fast Break Scorers against weak Fast Break Defenses: " + str((FBHitsU/FBTotalU) * 100))
        print("Total Sample Size: " + str(FBTotalU))
        print("Average odds of hits: " + str(FBoddsU / FBHitsU))
        profittotal = ((FBHitsU/FBTotalU) * 100) * (1 + (FBoddsU / FBHitsU)/100)
        profit = profittotal - 100
        rounded_profit = round(profit, 2)
        print("You would make/lose " + str(rounded_profit) + " if you bet 100 dollars on this trend")
        print('\n')
    if(TovTotalO == 0):
        print('No sample size')
    else:
        print("Turnover Scorers against weak Turnover Defenses: " + str((TovHitsU/TovTotalU) * 100))
        print("Total Sample Size: " + str(TovTotalU))
        print("Average odds of hits: " + str(TovoddsU / TovHitsU))
        profittotal = ((TovHitsU/TovTotalU) * 100) * (1 + (TovoddsU / TovHitsU)/100)
        profit = profittotal - 100
        rounded_profit = round(profit, 2)
        print("You would make/lose " + str(rounded_profit) + " if you bet 100 dollars on this trend")
        print('\n')
    if(SecondTotalO == 0):
        print('No sample size')
    else:
        print("Second Chance Scorers against Weak Second Chance Defenses: " + str((SecondHitsU/SecondTotalU) * 100))
        print("Total Sample Size: " + str(SecondTotalU))
        print("Total Sample Size: " + str(SecondTotalU))
        print("Average odds of hits: " + str(SecondoddsU / SecondHitsU))
        profittotal = ((SecondHitsU/SecondTotalU) * 100) * (1 + (SecondoddsU / SecondHitsU)/100)
        profit = profittotal - 100
        rounded_profit = round(profit, 2)
        print("You would make/lose " + str(rounded_profit) + " if you bet 100 dollars on this trend")
        print('\n')
    if(PaintTotalO == 0):
        print('No sample size')
    else:
        print("Paint Scorers against Weak Paint Defenses: " + str((PaintHitsU/PaintTotalU) * 100))
        print("Total Sample Size: " + str(PaintTotalU))
        print("Total Sample Size: " + str(PaintTotalU))
        print("Average odds of hits: " + str(PaintoddsU / PaintHitsU))
        profittotal = ((PaintHitsU/PaintTotalU) * 100) * (1 + (PaintoddsU / PaintHitsU)/100)
        profit = profittotal - 100
        rounded_profit = round(profit, 2)
        print("You would make/lose " + str(rounded_profit) + " if you bet 100 dollars on this trend")
        print('\n')
sys.stdout = original_stdout
#We now have all the box scores from yesterday, as well as all the results from yesterday
#empty players - certain players are listed one way on nba.com, but not always correctly listed in 
#sports books. We need to check for these every time, and manually fix them. We actually
#have used blanket fixes that should work. But when Bronny comes in it might need some changing
#Do the opposite of changed teams
#CONVERT the +odds into minus odds if they are less than 100