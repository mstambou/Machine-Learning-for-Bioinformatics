Today we will go over a [a realistic example](https://bugra.github.io/work/notes/2014-11-22/an-introduction-to-supervised-learning-scikit-learn/) written up by an experienced data scientist. This time we will walk through the process of obtaining, cleaning up and normalizing less-then-perfect data and comparing various classifiers with stratified cross validation.

A copy of the [churn dataset](churn.csv) used in the write up is included in this repo for your convenience.

Note that in the tutorial 
```python
from sklearn import cross_validation
```
is Deprecated and in the newer versions of python it is replaced by:
```python
from sklearn.model_selection import cross_val_score
```
