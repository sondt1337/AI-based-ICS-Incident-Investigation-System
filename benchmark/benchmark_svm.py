import pandas as pd
from sklearn.svm import SVC
from sklearn.model_selection import cross_val_score

data = pd.read_csv("Dataset.csv").dropna()
label = data['IT_B_Label']
data = data.select_dtypes('number').drop(columns = ['start', 'end', 'startOffset', 'endOffset', 'IT_B_Label', 'NST_B_Label'])

clf = SVC()
print(cross_val_score(clf, data, label).mean())

# 75% acc