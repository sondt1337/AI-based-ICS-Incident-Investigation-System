import pandas as pd
from xgboost import XGBClassifier
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler

data = pd.read_csv("Dataset.csv")
label = data['IT_M_Label'].map({'Normal': 0, 'ddos': 1, 'ip-scan': 2, 'mitm': 3, 'port-scan': 4, 'replay': 5})
data = data.select_dtypes('number').drop(columns = ['start', 'end', 'startOffset', 'endOffset', 'IT_B_Label', 'NST_B_Label'])

clf = Pipeline(steps = [
    ('preprocess', MinMaxScaler()),
    ('xgb', XGBClassifier(n_estimators = 10, max_depth = 50, learning_rate = 1, objective = 'multi:softmax'))
])
print(cross_val_score(clf, data, label).mean())

# 84% acc