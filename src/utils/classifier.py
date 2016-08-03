from textblob.classifiers import NaiveBayesClassifier
from textblob import TextBlob
from textblob.sentiments import *

class TextClassifier:

    _TRAIN_DATA = []

    TEST_DATA = []

    def feature_words(self):
        pass

    def extract_feature_words(self):
        pass

    def train_feature_words(self):
        cl = NaiveBayesClassifier(self._TRAIN_DATA)
        pass
    pass