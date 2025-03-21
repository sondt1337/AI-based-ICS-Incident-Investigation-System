import pandas as pd
from hyperopt import STATUS_OK, Trials, fmin, hp, tpe
from sklearn.model_selection import cross_val_score
from xgboost import XGBClassifier

data = pd.read_csv("Dataset.csv")
label = data['IT_M_Label'].map({'Normal': 0, 'ddos': 1, 'ip-scan': 2, 'mitm': 3, 'port-scan': 4, 'replay': 5})
data = data.select_dtypes('number').drop(columns = ['start', 'end', 'startOffset', 'endOffset', 'IT_B_Label', 'NST_B_Label'])

space = {
    'max_depth': hp.quniform("max_depth", 1, 30, 1),
    'gamma': hp.uniform ('gamma', 1, 9),
    'reg_alpha' : hp.quniform('reg_alpha', 40, 180, 1),
    'reg_lambda' : hp.uniform('reg_lambda', 0, 1),
    'colsample_bytree' : hp.uniform('colsample_bytree', 0.5, 1),
    'min_child_weight' : hp.quniform('min_child_weight', 0, 10, 1),
    'n_estimators': hp.quniform('n_estimators', 10, 200, 10),
    'seed': 0
}

def objective(space):
    clf = XGBClassifier(
        n_estimators = int(space['n_estimators']),
        max_depth = int(space['max_depth']),
        gamma = space['gamma'],
        reg_alpha = int(space['reg_alpha']),
        min_child_weight = int(space['min_child_weight']),
        colsample_bytree = int(space['colsample_bytree']),
        n_jobs = -1
    )
    
    accuracy = cross_val_score(clf, data, label).mean()
    print ("SCORE:", accuracy)
    return {'loss': -accuracy, 'status': STATUS_OK }

trials = Trials()

best_hyperparams = fmin(fn = objective,
                        space = space,
                        algo = tpe.suggest,
                        max_evals = 100,
                        trials = trials)

print(best_hyperparams)

# {'colsample_bytree': 0.5525886056747055, 'gamma': 1.489574337111725, 'max_depth': 20.0, 'min_child_weight': 3.0, 'n_estimators': 200.0, 'reg_alpha': 40.0, 'reg_lambda': 0.7917546280716226}

83.94