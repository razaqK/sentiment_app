from textblob.classifiers import NaiveBayesClassifier
from textblob import TextBlob
from textblob.sentiments import *

class TextClassifier:

    _TRAIN_DATA = [('I love this sandwich.', 'pos'),
         ('this is an amazing place!', 'pos'),
         ('I feel very good about these beers.', 'pos'),
         ('this is my best work.', 'pos'),
         ("what an awesome view", 'pos'),
         ('I do not like this restaurant', 'neg'),
         ('I am tired of this stuff.', 'neg'),
         ("I can't deal with this", 'neg'),
         ('he is my sworn enemy!', 'neg'),
         ('my boss is horrible.', 'neg'),
         ("He is a bad.", 'neg')]

    TEST_DATA = [('the beer was good.', 'pos'),
        ('I do not enjoy my job', 'neg'),
        ("I ain't feeling dandy today.", 'neg'),
        ("I feel amazing!", 'pos'),
        ('Gary is a friend of mine.', 'pos'),
        ("I can't believe I'm doing this.", 'neg')]

    def feature_words(self):
        pass

    def extract_feature_words(self):
        pass

    def train_feature_words(self):
        cl = NaiveBayesClassifier(self._TRAIN_DATA)
        blob = TextBlob("The beer is good. But the bad hangover.", classifier=cl)
        pass
