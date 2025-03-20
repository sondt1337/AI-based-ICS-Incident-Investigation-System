import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV

data = pd.read_csv("Dataset.csv")
label = data['IT_M_Label']
data['protocol'] = data['protocol'].map({'IPV4-TCP': 0, 'ARP': -1}).fillna(1)
data = data.select_dtypes('number').drop(columns = ['start', 'end', 'startOffset', 'endOffset', 'IT_B_Label', 'NST_B_Label'])

grid = GridSearchCV(RandomForestClassifier(), cv = 3, param_grid = {
    'n_estimators': [200],
    'max_depth': [30],
    'min_samples_split': [20],
    'n_jobs': [-1]
}, n_jobs = -1, verbose = 2)
grid.fit(data, label)
print(grid.cv_results_)
print(grid.best_params_)

data = pd.read_csv("env_test.csv")
data['protocol'] = data['protocol'].map({'IPV4-TCP': 0, 'ARP': -1}).fillna(1)
label = data['IT_M_Label']
data = data.select_dtypes('number').drop(columns = ['start', 'end', 'startOffset', 'endOffset', 'IT_B_Label', 'NST_B_Label'])

pred = grid.best_estimator_.predict(data)
# print(pred)

sns.heatmap(confusion_matrix(label, pred), annot = True, fmt = 'g')
plt.show()
print(grid.best_estimator_.score(data, label))