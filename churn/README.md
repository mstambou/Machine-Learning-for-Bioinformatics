Today we will go over a [a realistic example](https://bugra.github.io/work/notes/2014-11-22/an-introduction-to-supervised-learning-scikit-learn/) written up by an experienced data scientist. This time we will walk through the process of obtaining, cleaning up and normalizing less-then-perfect data and comparing various classifiers with stratified cross validation.

A copy of the [churn dataset](churn.csv) used in the write up is included in this repo for your convenience.

Note that in the tutorial 
```python
from sklearn import cross_validation
```
is Deprecated and in the newer versions of python it is replaced by:
```python
import sklearn.model_selection as cross_validation
```

for the stratified classifier use the following function as opposed the one in the blog. Some of the parameters have changed in the newer version of SK-learn
```python3
def stratified_cv(X, y, clf_class, shuffle=True, n_folds=10, **kwargs):
    skf = cross_validation.StratifiedKFold(n_splits=n_folds)
    y_pred = y.copy()
    for train, test in skf.split(X, y):        
        X_train, X_test = X[train], X[test]
        y_train = y[train]
        clf = clf_class(**kwargs)
        clf.fit(X_train,y_train)
        y_pred[test] = clf.predict(X_test)
    return y_pred
```
