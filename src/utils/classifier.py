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

    _CL = NaiveBayesClassifier(_TRAIN_DATA)

    response = {}
    info = []
    _LABEL = "company"
    _KEY_STMT = "sentence"
    _KEY_SENT = "sentiment"
    _KEY_HIGH_SENT = "sentiment_max"
    _KEY_POS_SENT = "sentiment_pos"
    _KEY_NEG_SENT = "sentiment_neg"

    def check_test_data_accuracy(self):
        return self._CL.accuracy(self.TEST_DATA)

    def trainer_sentiment(self, sentence):
        features = TextBlob(sentence, classifier=self._CL)

        for stmt in features.sentences:
            prob_dist = self._CL.prob_classify(stmt)
            self.response.update({self._LABEL: "walmart", self._KEY_STMT: stmt, self._KEY_SENT: stmt.classify(), self._KEY_HIGH_SENT: prob_dist.max(), self._KEY_POS_SENT: round(prob_dist.prob("pos"), 2), self._KEY_NEG_SENT: round(prob_dist.prob("neg"), 2)})
            """self.response[self._KEY_STMT] = stmt
            self.response[self._KEY_SENT] = stmt.classify()
            self.response[self._KEY_HIGH_SENT] = prob_dist.max()
            self.response[self._KEY_POS_SENT] = round(prob_dist.prob("pos"), 2)
            self.response[self._KEY_NEG_SENT] = round(prob_dist.prob("neg"), 2)"""
            self.info.append(self.response)

        return self.info

    def check_sentiment(self, sentence):
        status = self._CL.classify(sentence)
        return {"result": (sentence, status)}
    
    def load_words_list(self, filename):
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

"""sent = TextClassifier()
print(sent.trainer_sentiment("this is my best work. The man is boss, but bad fellow."))"""