import pickle
from sklearn.linear_model import LogisticRegression

class QuinielaModel:

    def __init__(self):
        self.model = LogisticRegression(max_iter=1000)
        self.teams = {}
    

    def setWinsDict(self, wins_dict):
        self.wins_dict = wins_dict


    def train(self, train_data):
        # Do something here to train the model
        x = train_data[['home_team', 'away_team', 'division', 'matchday', 'win_home', 'win_away']].copy(deep=True)
        y = train_data['result']
        
        for count, team in enumerate(x['home_team'].unique()):
            self.teams[team] = count

        x['home_team'] = x['home_team'].map(self.teams)
        x['away_team'] = x['away_team'].map(self.teams)

        self.model.fit(x, y)
        

    def predict(self, predict_data):
        
        x = predict_data[['home_team', 'away_team', 'division', 'matchday', 'win_home', 'win_away']].copy(deep=True)

        x['home_team'] = x['home_team'].map(self.teams)
        x['away_team'] = x['away_team'].map(self.teams)
        x.fillna(-1, inplace=True)

        prediction = self.model.predict(x)

        return prediction

    @classmethod
    def load(cls, filename):
        """ Load model from file """
        with open(filename, "rb") as f:
            model = pickle.load(f)
            assert type(model) == cls
        return model

    def save(self, filename):
        """ Save a model in a file """
        with open(filename, "wb") as f:
            pickle.dump(self, f)
