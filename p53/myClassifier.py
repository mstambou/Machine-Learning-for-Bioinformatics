# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 17:57:52 2019

@author: mstambou
"""

import pandas as pd
import numpy as np

from sklearn import preprocessing

from sklearn import ensemble

from scipy import interp
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc
from sklearn.model_selection import StratifiedKFold

from sklearn.decomposition import PCA

n_pcs = 100

data_in = 'Data Sets/K9.data'

k9_data_df = pd.read_csv(data_in, sep = ',', header = None)

clean_k9_data_df = k9_data_df[~(k9_data_df == '?').any(axis=1)]
clean_k9_data_df.to_csv('Data Sets/clean_K9.data', sep = ',', header= None, index = False)

clean_k9_data_df = pd.read_csv('Data Sets/clean_K9.data', sep = ',', header= None)

y = clean_k9_data_df[5408]
y = [1.0 if item == 'active' else 0.0 for item in y]
X = clean_k9_data_df.loc[:, :5407]

X = X.as_matrix().astype(np.float)
y = np.asarray(y)
#y=y.transpose()
scaler = preprocessing.StandardScaler()
X = scaler.fit_transform(X)

y_col = pd.DataFrame({'class':y})

cols = ['PC'+str(i) for i in range(1, n_pcs+1)]
pca = PCA(n_components=n_pcs)
principalComponents = pca.fit_transform(X)
principalDf = pd.DataFrame(data = principalComponents, columns = cols)
finalDf = pd.concat([principalDf, y_col['class']], axis = 1)

pca_x = finalDf.loc[:, cols].values

cv = StratifiedKFold(n_splits=10)
clf = ensemble.RandomForestClassifier(n_estimators = 100)


tprs = []
aucs = []
mean_fpr = np.linspace(0, 1, 100)

i = 0
for train, test in cv.split(pca_x, y):
    probas_ = clf.fit(pca_x[train], y[train]).predict_proba(pca_x[test])
    # Compute ROC curve and area the curve
    fpr, tpr, thresholds = roc_curve(y[test], probas_[:, 1])
    tprs.append(interp(mean_fpr, fpr, tpr))
    tprs[-1][0] = 0.0
    roc_auc = auc(fpr, tpr)
    aucs.append(roc_auc)
    plt.plot(fpr, tpr, lw=1, alpha=0.3,
             label='ROC fold %d (AUC = %0.2f)' % (i, roc_auc))
    i += 1

plt.figure(figsize = (8,8))
plt.plot([0, 1], [0, 1], linestyle='--', lw=2, color='r',
         label='Chance', alpha=.8)

mean_tpr = np.mean(tprs, axis=0)
mean_tpr[-1] = 1.0
mean_auc = auc(mean_fpr, mean_tpr)
std_auc = np.std(aucs)
plt.plot(mean_fpr, mean_tpr, color='b',
         label=r'Mean ROC (AUC = %0.2f $\pm$ %0.2f)' % (mean_auc, std_auc),
         lw=2, alpha=.8)

std_tpr = np.std(tprs, axis=0)
tprs_upper = np.minimum(mean_tpr + std_tpr, 1)
tprs_lower = np.maximum(mean_tpr - std_tpr, 0)
plt.fill_between(mean_fpr, tprs_lower, tprs_upper, color='grey', alpha=.2,
                 label=r'$\pm$ 1 std. dev.')

plt.xlim([-0.05, 1.05])
plt.ylim([-0.05, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver operating characteristic example')
plt.legend(loc="lower right")
plt.tight_layout()
plt.savefig('RF100_classifier.png')