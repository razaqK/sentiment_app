from textblob.classifiers import NaiveBayesClassifier
from textblob import TextBlob
from textblob.sentiments import *

class TextClassifier:

    TRAIN_DATA = []

    TEST_DATA = []

    cl = NaiveBayesClassifier(TRAIN_DATA)
    pass