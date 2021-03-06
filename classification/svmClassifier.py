# svmClassifier.py
# ---------------

# adapted by Richard Guo, for CPS 270
# guo@cs.duke.edu

import util
import classificationMethod
from sklearn import svm, grid_search    # you can use scikit-learn as a module in this assignment. You are free to import more stuff from sklearn.
import numpy as np                      # you are also allowed to use the numerical module "numpy" (e.g. for computing mean and std)
from math import sqrt					# you may need this

class SupportVectorMachineClassifier(classificationMethod.ClassificationMethod):
  """
  The SVM classifier based on scikit-learn.
  """
  def __init__(self, legalLabels):
    self.type = "svm"

    print "\nSVM classifier working now...\n"

  def formattingData(self, data, features, mean=None, std=None):
    '''
    Convert data in the form of a list of dict to a n x p list of list object,
    which is used by scikit-learn. n is the number of training samples and p is the number of features.
    And normalize data with given mean and std so that each feature has mean 0 and std 1.

    features: the list of features

    mean, std: both are dictionaries indexed by features.
    If mean==None, mean is set to all zero; if std==None, std is set to all one.

    * Hint:
    Normalizing each feature to have mean 0 and sd 1 can enhance the performance of SVM.
    '''
    if mean==None:
      mean = dict((u, 0.0) for u in features)
    if std==None:
      std = dict((u, 1.0) for u in features)

    return [[(datum[u] - mean[u])/std[u] for u in features] for datum in data]


  def train(self, trainingData, trainingLabels, validationData, validationLabels):
    """
    Fill out your code here to train a SVM classifier.

    To have your classifier *continue to live* after training, write something like "self.myclassifier".

    You may need to call formattingData(...) to convert trainingData to an appropriate form for scikit-learn.

    trainingData: A list [datum_1, datum_2, ...], with datum_i being i-th sample.
                  Each datum_i is a dictionary in the form of {feature_k: value_k}

    trainingLabels: A list of class lables (integers 0 - 9), of the same length as trainingData

    validationData: validation set of data, of the same type as trainingData

    validationLabels: validation class labels, of the same tyoe as trainingLabels

    No returning value is needed in this method.
    """

    # might be useful in your code later...
    # this is a list of all features in the training set.
    self.features = list(set([ f for datum in trainingData for f in datum.keys() ]))

    "*** YOUR CODE HERE ***"
    # start with training data
    formattedTrainingData = self.formattingData(trainingData, self.features)

    # take in two params for svc (gamma and c) s
    # first find possible ranges for gamma and c
    # use numpy (np)
    gammaRange = np.logspace(-9,3,13)
    cRange = np.logspace(-2,10,13)
    # search over a grid using quickstart's rbf and linear params
    # print estimator.get_params().keys()
    gridToSearch = dict(gamma = gammaRange, C = cRange, kernel = ['rbf', 'linear'])
    searchedGrid = grid_search.GridSearchCV(svm.SVC(), param_grid = gridToSearch)
    # fit using input data + labels
    searchedGrid.fit(formattedTrainingData, trainingLabels)
    cFit = searchedGrid.best_params_["C"] # grab best fit c value
    if "gamma" in searchedGrid.best_params_.keys():
        gammaFit = searchedGrid.best_params_["gamma"]
        self.clf = svm.SVC(C = cFit, kernel = 'rbf', gamma = gammaFit)
    else:
        self.clf = svm.SVC(C = cFit, kernel = searchedGrid.best_params_["kernel"])
    self.clf.fit(formattedTrainingData, trainingLabels)

  def classify(self, testData):
    """
    Use the trained SVM classifier to predict the class labels of testData.

    testData: test dataset of the same type as trainingData in self.train(...)

    return: a list of predicted class labels.
    """

    "*** YOUR CODE HERE ***"
    # normalize features using formatittingData method
    formattedData = self.formattingData(testData, self.features)
    formattedPrediction = self.clf.predict(formattedData)
    return formattedPrediction
