import sqlite3
import pandas as pd
import numpy as np
import settings


def load_matchday(season, division, matchday):
    with sqlite3.connect(settings.DATABASE_PATH) as conn:
        data = pd.read_sql(f"""
            SELECT * FROM Matches
                WHERE season = '{season}'
                  AND division = {division}
                  AND matchday = {matchday}
        """, conn)
    if data.empty:
        raise ValueError("There is no matchday data for the values given")
    return data


def load_historical_data(seasons):
    with sqlite3.connect(settings.DATABASE_PATH) as conn:
        if seasons == "all":
            data = pd.read_sql("SELECT * FROM Matches", conn)
        else:
            data = pd.read_sql(f"""
                SELECT * FROM Matches
                    WHERE season IN {tuple(seasons)}
            """, conn)
    if data.empty:
        raise ValueError(f"No data for seasons {seasons}")
    return data


def add_result(data):
    data[['goals_home', 'goals_away']] = data['score'].str.split(':', expand=True).astype(int)
    results = [
        (data['goals_home'] > data['goals_away']),
        (data['goals_home'] == data['goals_away']),
        (data['goals_home'] < data['goals_away'])
    ]

    data['result'] = np.select(results, [1, 0, 2])
    return data


def count_wins(data):
    wins_dictionary = { team:0 for team in data['home_team'].unique()}

    data['win_home'] = 0
    data['win_away'] = 0

    for index, partido in data.iterrows():
        home_team = partido['home_team']
        away_team = partido['away_team']
        
        if partido['result'] == 1:
            wins_dictionary[home_team] += 1
        elif partido['result'] == 2:
            wins_dictionary[away_team] += 1

        data.at[index, 'win_home'] = wins_dictionary[home_team]
        data.at[index, 'win_away'] = wins_dictionary[away_team]

    return data, wins_dictionary


def add_wins(data, wins_dict):
    data['win_home'] = 0
    data['win_away'] = 0

    for index, partido in data.iterrows():
        home_team = partido['home_team']
        away_team = partido['away_team']

        if home_team in wins_dict:
            data.at[index, 'win_home'] = wins_dict[home_team]
        if away_team in wins_dict:
            data.at[index, 'win_away'] = wins_dict[away_team]

    return data


def drop_created_columns(data):
    data.drop(['win_home', 'win_away'], inplace=True, axis=1)
    return data


def save_predictions(predictions):
    with sqlite3.connect(settings.DATABASE_PATH) as conn:
        predictions.to_sql(name="Predictions", con=conn, if_exists="append", index=False)
