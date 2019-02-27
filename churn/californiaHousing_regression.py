# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 20:50:44 2019

@author: mstambou
"""

from sklearn.datasets.california_housing import fetch_california_housing
import sklearn

california_housing = sklearn.datasets.california_housing.fetch_california_housing()
california_housing_data = california_housing['data']
california_housing_labels = california_housing['target']# 'target' variables
california_housing_feature_names = california_housing['feature_names']

california_housing_feature_names

from sklearn import cross_validation
X_train, X_test, y_train, y_test = cross_validation.train_test_split(california_housing_data,
                                                    california_housing_labels,
                                                    test_size=0.2,
                                                    random_state=0)

print(X_train.shape)
print(X_test.shape)
print('Training/Test Ratio: {}'.format(X_train.shape[0] / X_test.shape[0]))

parameters = {
              'n_estimators': 500, 
              'max_depth': 4, 
              'min_samples_split': 1.0,
              'learning_rate': 0.01, 
              'loss': 'ls'
             }

from sklearn import ensemble
from sklearn import metrics
classifier = ensemble.GradientBoostingRegressor(**parameters)

classifier.fit(X_train, y_train)
predictions = classifier.predict(X_test)
mse = metrics.mean_squared_error(y_test, predictions)
print('Mean Square Error: {:.3f}'.format(mse))

parameters = {
              'n_estimators': 3000, 
              'max_depth': 6, 
              'learning_rate': 0.04, 
              'loss': 'huber'
             }
classifier = ensemble.GradientBoostingRegressor(**parameters)

classifier.fit(X_train, y_train)
predictions = classifier.predict(X_test)
mse = metrics.mean_squared_error(y_test, predictions)
print('Mean Squared Error: {:.3f}'.format(mse))

import matplotlib.pyplot as plt
import numpy as np

plt.figure(figsize=(16, 12))

plt.scatter(range(predictions.shape[0]), predictions, label='predictions', c='#348ABD', alpha=0.4)
plt.scatter(range(y_test.shape[0]), y_test, label='actual values', c='#A60628', alpha=0.4)
plt.ylim([y_test.min(), predictions.max()])
plt.xlim([0, predictions.shape[0]])
plt.legend();

test_score = [classifier.loss_(y_test, y_pred) for y_pred in classifier.staged_predict(X_test)]

plt.figure(figsize=(16, 12))
plt.title('Deviance');
plt.plot(np.arange(parameters['n_estimators']) + 1, classifier.train_score_, c='#348ABD',
         label='Training Set Deviance');
plt.plot(np.arange(parameters['n_estimators']) + 1, test_score, c='#A60628',
         label='Test Set Deviance');
plt.annotate('Overfit Point', xy=(600, test_score[600]), xycoords='data',
            xytext=(420, 0.06), textcoords='data',
            arrowprops=dict(arrowstyle="->", connectionstyle="arc"),
            )
plt.legend(loc='upper right');
plt.xlabel('Boosting Iterations');
plt.ylabel('Deviance');

# Get Feature Importance from the classifier
feature_importance = classifier.feature_importances_
# Normalize The Features
feature_importance = 100.0 * (feature_importance / feature_importance.max())
sorted_idx = np.argsort(feature_importance)
pos = np.arange(sorted_idx.shape[0]) + .5
plt.figure(figsize=(16, 12))
plt.barh(pos, feature_importance[sorted_idx], align='center', color='#7A68A6')
plt.yticks(pos, np.asanyarray(california_housing_feature_names)[sorted_idx])
plt.xlabel('Relative Importance')
plt.title('Variable Importance')
plt.show()

features = ['MedInc', 'AveOccup', 'HouseAge', 'AveRooms',
            ('AveOccup', 'HouseAge')]
fig, ax = ensemble.partial_dependence.plot_partial_dependence(classifier, X_train, features, 
                                                              feature_names=california_housing_feature_names, 
                                                              figsize=(16, 12));
