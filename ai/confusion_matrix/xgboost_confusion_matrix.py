import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import torch
from xgboost import XGBClassifier, plot_tree
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, f1_score

protocol_map = {'Normal': 0, 'ddos': 1, 'ip-scan': 2, 'mitm': 3, 'port-scan': 4, 'replay': 5, 'command-injection': 6}
protocols = ['Normal', 'ddos', 'ip-scan', 'mitm', 'port-scan', 'replay', 'command-injection']

data = pd.concat([pd.read_csv("pcaps/extra_training.csv"), pd.read_csv("pcaps/extra_training2.csv")])
# data = pd.read_csv("ai/Dataset.csv")
# label = data['IT_B_Label']
label = data['IT_M_Label'].map(protocol_map)
data['protocol'] = data['protocol'].map({'IPV4-TCP': 1, 'ARP': -1}).fillna(0)
data = data.select_dtypes('number').drop(columns = ['start', 'end', 'startOffset', 'endOffset', 'IT_B_Label', 'NST_B_Label'])

X_train, X_test, y_train, y_test = train_test_split(data, label, test_size = 0.2, random_state = 0)

bst = XGBClassifier(n_estimators = 300, max_depth = 5, learning_rate = 1, objective = 'multi:softmax', gamma = 1, reg_alpha = 0.1, n_jobs = -1)
# bst = XGBClassifier(n_estimators = 300, max_depth = 5, learning_rate = 1, objective = 'reg:logistic', gamma = 1, reg_alpha = 0.1, n_jobs = -1)

bst = bst.fit(X_train, y_train)

# print(bst.score(X_train, y_train))
# pred = bst.predict(X_train)
# sns.heatmap(confusion_matrix(y_train, pred), annot = True, fmt = 'g', xticklabels = protocols, yticklabels = protocols)
# plt.xlabel('Prediction', size = 20)
# plt.ylabel('Attack type', size = 20)
# plt.xticks(rotation = 0, size = 16) 
# plt.yticks(size = 16) 
# plt.show()

pred = bst.predict(X_test)
print(bst.score(X_test, y_test))
plot_tree(bst)
# print(bst.feature_importances_)
plt.show()

# sns.heatmap(confusion_matrix(y_test, pred), annot = True, fmt = 'g', xticklabels = protocols, yticklabels = protocols)
# plt.xlabel('Prediction', size = 20)
# plt.ylabel('Attack type', size = 20)
# plt.xticks(rotation = 0, size = 16) 
# plt.yticks(size = 16) 
# plt.show()

test_file = "pcaps/traffic.csv"

data = pd.read_csv(test_file)
data['protocol'] = data['protocol'].map({'IPV4-TCP': 1, 'ARP': -1}).fillna(0)
# label = data['IT_B_Label']
# label = data['IT_M_Label'].map(protocol_map)
# label = [0] * data.shape[0]
data = data.select_dtypes('number').drop(columns = ['start', 'end', 'startOffset', 'endOffset',
                                                    # 'IT_B_Label', 'NST_B_Label'
                                                    ])

pred = bst.predict(data)
# print(bst.score(data, label))

# sns.heatmap(confusion_matrix(label, pred), annot = True, fmt = 'g')
# plt.show()

bad = []
attack = []
for i, type in enumerate(pred):
    if type != 0:
        bad.append(i)
        attack.append(protocols[type])
data = pd.read_csv(test_file)
data = data.iloc[bad][['sAddress', 'rAddress', 'protocol', 'startDate', 'endDate']]
data['attack'] = attack
data.to_csv('out.csv')