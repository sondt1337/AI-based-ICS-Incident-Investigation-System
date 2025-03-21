import pandas as pd
from xgboost import XGBClassifier
from sklearn.model_selection import cross_val_score

data = pd.read_csv("Dataset.csv")
label = data['IT_M_Label'].map({'Normal': 0, 'ddos': 1, 'ip-scan': 2, 'mitm': 3, 'port-scan': 4, 'replay': 5})
data['protocol'] = data['protocol'].map({'IPV4-TCP': 1, 'ARP': -1}).fillna(0)
data = data.select_dtypes('number').drop(columns = ['start', 'end', 'startOffset', 'endOffset', 'IT_B_Label', 'NST_B_Label'])

bst = XGBClassifier(n_estimators = 200, max_depth = 10, learning_rate = 1, objective = 'multi:softmax', n_jobs = -1)

print(cross_val_score(bst, data, label).mean())