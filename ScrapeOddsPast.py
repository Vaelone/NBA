import requests
import urllib
from datetime import datetime, timedelta
import json
import pandas as pd

BASE_URL = 'https://api.prop-odds.com'
API_KEY = 'dUGoVymuEFB7b1pigNlG6xUkCsAXFpZV21w'


def get_request(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()

    print('Request failed with status:', response.status_code)
    return {}


def get_nba_games(date):
    query_params = {
        'date': date.strftime('%Y-%m-%d'),
        'tz': 'America/New_York',
        'api_key': API_KEY,
    }
    params = urllib.parse.urlencode(query_params)
    url = BASE_URL + '/beta/games/nba?' + params
    return get_request(url)


def get_game_info(game_id):
    query_params = {
        'api_key': API_KEY,
    }
    params = urllib.parse.urlencode(query_params)
    url = BASE_URL + '/beta/game/' + game_id + '?' + params
    return get_request(url)


def get_markets(game_id):
    query_params = {
        'api_key': API_KEY,
    }
    params = urllib.parse.urlencode(query_params)
    url = BASE_URL + '/beta/markets/' + game_id + '?' + params
    return get_request(url)


def get_most_recent_odds(game_id, market, end_datetime):
    query_params = {
        'api_key': API_KEY,
        'end_datetime': end_datetime
    }
    params = urllib.parse.urlencode(query_params)
    url = BASE_URL + '/beta/odds/' + game_id + '/' + market + '?' + params
    return get_request(url)


def main():
    start_date = datetime(2023, 10, 24)
    end_date = datetime(2024, 1, 17)
    gamecount = 0
    daycount = 0
    current_date = start_date
    complete_df_list = []
    oddscheck = False
    while current_date <= end_date:
        games = get_nba_games(current_date)
        if not games['games']:
            print(f"No games available for {current_date}")
            current_date += timedelta(days=1)
            continue
        final_df_list = []
        for game in games['games']:
            game_id = game['game_id']
            start_time = game['start_timestamp']
            team_df = pd.DataFrame({
            'AwayTeam': game['away_team'],
            'HomeTeam': game['home_team']
            }, index=[0])
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
            team_df['AwayTeam'] = team_df['AwayTeam'].map(team_abbreviations)
            team_df['HomeTeam'] = team_df['HomeTeam'].map(team_abbreviations)
            markets = ['player_assists_over_under', 'player_assists_points_over_under', 
                   'player_assists_points_rebounds_over_under', 'player_assists_rebounds_over_under',
                   'player_blocks_over_under',  'player_blocks_steals_over_under' ,
                   'player_points_over_under', 'player_points_rebounds_over_under', 
                   'player_rebounds_over_under', 'player_steals_over_under', 
                   'player_threes_over_under', 'player_turnovers_over_under']
            for market in markets:
                odds = get_most_recent_odds(game_id, market, start_time)
                if not odds:
                    oddscheck = True
                    continue
                barstool_outcomes = [outcome for sportsbook in odds['sportsbooks'] if sportsbook['bookie_key'] == 
                                            'barstool' for outcome in sportsbook['market']['outcomes']]

                result_df = pd.DataFrame(barstool_outcomes)
                # # Convert the timestamp to a datetime object
                result_df['timestamp'] = pd.to_datetime(result_df['timestamp'])
                # Display the resulting DataFrame
                result_df = result_df[result_df['participant'].notna()]
                final_df = pd.concat([result_df, team_df], axis=1)
                final_df = final_df.fillna(method='ffill')
                final_df['AwayTeam'] = final_df['AwayTeam'].fillna(team_df['AwayTeam'].iloc[0])
                final_df['HomeTeam'] = final_df['HomeTeam'].fillna(team_df['HomeTeam'].iloc[0])

                final_df_list.append(final_df)
                #We can rename final_df to game_df
            gamecount+=1
            print("game " + str(gamecount) + " done")
        if(oddscheck):
            continue
        complete_df = pd.concat(final_df_list, ignore_index=True)
        columns_to_remove = ['timestamp', 'participant']
        complete_df = complete_df.drop(columns=columns_to_remove)   
        complete_df.reset_index(drop=True, inplace=True) 
        complete_df = complete_df[(complete_df['odds'] >= -170) & (complete_df['odds'] <= 150)]
        complete_df['description'] = complete_df['description'].str.replace(r'^.*Total', 'Total', regex=True)
        complete_df['participant_name'] = complete_df['participant_name'].apply(lambda x: ' '.join(x.split()[:2]))
        complete_df['participant_name'] = complete_df['participant_name'].str.lower()
        complete_df['participant_name'] = complete_df['participant_name'].str.replace('nicolas claxton', 'nic claxton', case=False)
        complete_df['participant_name'] = complete_df['participant_name'].str.replace('cameron thomas', 'cam thomas', case=False)
        complete_df['game_date'] = current_date
        complete_df_list.append(complete_df)
        #We can rename complete_df to date_df
        daycount+=1
        print(str(current_date) + " done")
        current_date += timedelta(days=1)
    odds = pd.concat(complete_df_list, ignore_index=True)
    def convert_odds(value):
        if value < 0:
            return (100 / abs(int(value))) * 100
        else:
            return int(value)

    # Apply the conversion function to the 'results' column
    odds['odds'] = odds['odds'].apply(convert_odds)
    # if len(games['games']) == 0:
    #     print('No games scheduled for today.')
    #     return

    # first_game = games['games'][0]
    # game_id = first_game['game_id']


    odds.to_csv('rawodds.csv', index=False)
    

    

if __name__ == '__main__':
    main()