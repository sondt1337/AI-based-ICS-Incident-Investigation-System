import pandas as pd
from sklearn.model_selection import GridSearchCV
from xgboost import XGBClassifier

data = pd.read_csv("Dataset.csv")
label = data['IT_M_Label'].map({'Normal': 0, 'ddos': 1, 'ip-scan': 2, 'mitm': 3, 'port-scan': 4, 'replay': 5})
data = data.select_dtypes('number').drop(columns = ['start', 'end', 'startOffset', 'endOffset', 'IT_B_Label', 'NST_B_Label'])

params = {
    'learning_rate': [0.1, 0.3, 0.5],
    'gamma': [0, 3, 5],
    'max_depth': [3, 6, 10, 20],
    'min_child_weight': [0.5, 1, 2],
}

clf = GridSearchCV(XGBClassifier(n_jobs = -1), params)
clf.fit(data, label)
print(clf.cv_results)