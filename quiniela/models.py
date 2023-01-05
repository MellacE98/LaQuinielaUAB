import pickle
from sklearn.ensemble import RandomForestClassifier

class QuinielaModel:

    def __init__(self):
        self.model = RandomForestClassifier()
        self.teams = {}

    def train(self, train_data):
        # Do something here to train the model
        x = train_data[['home_team', 'away_team', 'division', 'matchday']].copy(deep=True)
        y = train_data['result']
        
        for count, team in enumerate(x['home_team'].unique()):
            self.teams[team] = count

        x['home_team'] = x['home_team'].map(self.teams)
        x['away_team'] = x['away_team'].map(self.teams)

        self.model.fit(x, y)
        

    def predict(self, predict_data):
        
        x = predict_data[['home_team', 'away_team', 'division', 'matchday']].copy(deep=True)

        x['home_team'] = x['home_team'].map(self.teams)
        x['away_team'] = x['away_team'].map(self.teams)

        results = []
        prediction = self.model.predict(x)
        
        for i in list(predict_data['score']):
            result = i.split(':')
            if float(result[0]) > float(result[1]):
                results.append(1)
            elif float(result[0]) < float(result[1]):
                results.append(2)
            else:
                results.append(0)

        print(prediction)
        print(results)
        print()
        print([prediction[i] == results[i] for i in range(len(results))])
        return ['X' for i in range(len(predict_data))]

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
