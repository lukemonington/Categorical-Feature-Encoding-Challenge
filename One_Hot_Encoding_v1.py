import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.feature_extraction import FeatureHasher
from sklearn.model_selection import train_test_split
pd.set_option('max_columns', None)
import xgboost as xgb
from xgboost import XGBClassifier
import eli5
from eli5.sklearn import PermutationImportance

# Get train and test dataset
df_train = pd.read_csv('C:/Users/lukem/Desktop/AI Projects/Categorical Feature Encoding Challenge/train.csv')
df_test = pd.read_csv('C:/Users/lukem/Desktop/AI Projects/Categorical Feature Encoding Challenge/test.csv')

# Set up our X and y for our training set
X = df_train.drop(columns=['id', 'target'])
y = df_train['target']
test = df_test.drop(columns=['id'])
labels = X.columns
IDs = df_test['id']

print("Training set shape: {} \nTest set shape: {}".format(X.shape, test.shape))

for f in X.columns:
    if X[f].dtype == "object" or test[f].dtype == "object":
        lr = LabelEncoder()
        lr.fit(list(X[f]) + list(test[f]))
        X[f] = lr.transform(X[f])
        test[f] = lr.transform(test[f])
        
        
clf = xgb.XGBClassifier(
    n_estimators=500,
    max_depth=9,
    learning_rate=0.05,
    subsample=0.9,
    colsample_bytree=0.9,
    missing=-999,
    random_state=2019,
    tree_method='gpu_hist'  # THE MAGICAL PARAMETER
)

X_train, X_val, y_train, y_val = train_test_split(X, y, test_size = 0.2)
%time clf.fit(X_train, y_train)

perm = PermutationImportance(clf, random_state=1).fit(X_val, y_val)
# Store feature weights in an object
html_obj = eli5.show_weights(perm, feature_names = X_val.columns.tolist())
with open(r'C:\Users\lukem\Desktop\Github AI Projects\Categorical-Feature-Encoding-Challenge\cat-feature-importance.htm','wb') as f:
    f.write(html_obj.data.encode("UTF-8"))


pred = clf.predict(test)
    

# Creating submission csv file
submission = pd.DataFrame(IDs, columns = ['id'])
submission['target'] = pred
submission.head()

# pd.get_dummies
path = r'C:\Users\lukem\Desktop\Github AI Projects\Submissions\Cat Feature Encoding Challenge\ '
submission.to_csv(path + 'submission v1.csv', index = False)
























































