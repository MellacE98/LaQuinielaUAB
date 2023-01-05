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


def modify_data(data):
    data[['goals_home', 'goals_away']] = data['score'].str.split(':', expand=True).astype(int)
    
    results = [
        (data['goals_home'] > data['goals_away']),
        (data['goals_home'] == data['goals_away']),
        (data['goals_home'] < data['goals_away'])
    ]
    
    data['result'] = np.select(results, [1,  0, 2])
    return data
    

def save_predictions(predictions):
    with sqlite3.connect(settings.DATABASE_PATH) as conn:
        predictions.to_sql(name="Predictions", con=conn, if_exists="append", index=False)
