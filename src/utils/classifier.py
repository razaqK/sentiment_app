from textblob.classifiers import NaiveBayesClassifier
from textblob import TextBlob
import json
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

    cl = NaiveBayesClassifier(_TRAIN_DATA)

    def load_words_list(self, filename):
        pass

    def feature_words(self):
        pass

    def extract_feature_words(self):
        pass

    def train_feature_words(self, features):
        blob = TextBlob(features, classifier=self.cl)
        for s in blob.sentences:
            print(s)
            print(s.classify())

    def update_train_data(self, data):
        self.cl.update(data)

    def check_sent_accuracy(self):
        self.cl.accuracy(self.TEST_DATA)

    def clasify_sent(self, sentence):
        self.cl.classify(sentence)

    def check_sent(self):
        print(self.cl.classify("He ain't from around here.!"))
        prob_dist = self.cl.prob_classify("This one's a doozy.")
        prob_dist.max()
        round(prob_dist.prob("pos"), 2)
        round(prob_dist.prob("neg"), 2)

    def get_sentiment(self, message):
        text = TextBlob(message)
        response = {'polarity': text.polarity, 'subjectivity': text.subjectivity}
        return json(response)
