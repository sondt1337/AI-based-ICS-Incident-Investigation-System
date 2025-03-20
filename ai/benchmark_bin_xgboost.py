import pandas as pd
from xgboost import XGBClassifier
from sklearn.model_selection import cross_val_score

data = pd.read_csv("Dataset.csv")
label = data['IT_B_Label']
data = data.select_dtypes('number').drop(columns = ['start', 'end', 'startOffset', 'endOffset', 'IT_B_Label', 'NST_B_Label'])

bst = XGBClassifier(n_estimators = 10, max_depth = 50, learning_rate = 1, objective = 'binary:logistic')

print(cross_val_score(bst, data, label).mean())

# 85% acc