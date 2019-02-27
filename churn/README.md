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
def stratified_cv(X, y, clf_class, shuffle=True, n_splits=10, **kwargs):
    stratified_k_fold = cross_validation.StratifiedKFold(y, n_splits=n_splits, shuffle=shuffle)
    y_pred = y.copy()
    for ii, jj in stratified_k_fold:
        X_train, X_test = X[ii], X[jj]
        y_train = y[ii]
        clf = clf_class(**kwargs)
        clf.fit(X_train,y_train)
        y_pred[jj] = clf.predict(X_test)
    return y_pred
```
