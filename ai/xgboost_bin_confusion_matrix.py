import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix

data = pd.read_csv("Dataset.csv")
label = data['IT_B_Label']
data['protocol'] = data['protocol'].map({'IPV4-TCP': 1, 'ARP': -1}).fillna(0)
data = data.select_dtypes('number').drop(columns = ['start', 'end', 'startOffset', 'endOffset', 'IT_B_Label', 'NST_B_Label'])

X_train, X_test, y_train, y_test = train_test_split(data, label, test_size = 0.2)

bst = XGBClassifier(n_estimators = 200, max_depth = 10, learning_rate = 1, objective = 'binary:logistic', n_jobs = -1)

bst = bst.fit(X_train, y_train)
pred = bst.predict(X_test)

sns.heatmap(confusion_matrix(y_test, pred), annot = True, fmt = 'g')
plt.show()

# combine into bin normal ~88%

data = pd.read_csv("env_test.csv")
data['protocol'] = data['protocol'].map({'IPV4-TCP': 1, 'ARP': -1}).fillna(0)
data = data.select_dtypes('number').drop(columns = ['start', 'end', 'startOffset', 'endOffset'])

pred = bst.predict(data)
print(pred)