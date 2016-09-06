import unittest

import datetime, os, sys

parent_path = os.path.abspath("..")
if parent_path not in sys.path:
    sys.path.insert(0, parent_path)

from src import pulldata
from src import utils.classifier as classify
class DataTest(unittest.TestCase):
    def setUp(self):
        self.data_pull = pulldata.PullData()
        self.classifier = classify.TextClassifier()
        self.config = pulldata.Config()
        self.credentials = self.config.read_config()
        self.graph_url = "https://graph.facebook.com/walmart"
        self.graph_url1 = "https://graph.facebook.com/"
        self.APP_ID = self.credentials[0]
        self.APP_SECRET = self.credentials[1]
        self.last_crawl = datetime.datetime.now() - datetime.timedelta(days=2)
        self.last_crawl = self.last_crawl.isoformat()
        self.URL = "https://graph.facebook.com/walmart/?key=value&access_token=2040068469550624|bc5698075f791582c6e5fb9dbc0f144b"
        self.URL1 = "https://graph.facebook.com/walmart/posts/?key=value&access_token=2040068469550624|bc5698075f791582c6e5fb9dbc0f144b"
        self.URL2 = "https://graph.facebook.com/159616034235_10154463822269236/comments/?key=value&access_token=2040068469550624|bc5698075f791582c6e5fb9dbc0f144b"
        self.url_output = { "name": "Walmart", "id": "159616034235"}
        self.scrape_output = [['159616034235_10154463822269236', 'Save money on all the stylish back-to-school accessories, like 2-pocket Character Backpacks.', '2016-07-12T22:08:03+0000'], ['159616034235_10154463969304236', 'Save more and start the semester off right with items like the Samsung Chromebook.', '2016-07-12T22:06:13+0000'], ['159616034235_10154449918839236', 'Nunca es muy pronto para pensar en el regreso a clases. Invierte en el desarollo de tus hijos con artículos escolares. Encuéntralos a precios bajos todos los días en Walmart.', '2016-07-11T13:00:00+0000'], ['159616034235_10154449918839236', 'Nunca es muy pronto para pensar en el regreso a clases. Invierte en el desarollo de tus hijos con artículos escolares. Encuéntralos a precios bajos todos los días en Walmart.', '2016-07-11T13:00:00+0000'], ['159616034235_10154449672509236', 'Do you know Troy? He’s the store manager at your relocated Lodi Walmart Supercenter opening on July 13 at 1600 Westgate Drive. Tell Troy “hi” below and “like” your local page for more info! https://www.facebook.com/Walmart1789', '2016-07-06T16:30:00+0000']]
        self.POST_DATA = []
        self.COMMENT_DATA = []
        self.POST_ID = '159616034235_10154463822269236'
        self.CONFIG_RESULT = ['bc5698075f791582c6e5fb9dbc0f144b', '2040068469550624']
        self.READ_CONFIG_RESULT = ['APP_SECRET = bc5698075f791582c6e5fb9dbc0f144b\n', 'APP_ID = 2040068469550624']
        self.TEST_DATA = [('the beer was good.', 'pos'),
                     ('I do not enjoy my job', 'neg'),
                     ("I ain't feeling dandy today.", 'neg'),
                     ("I feel amazing!", 'pos'),
                     ('Gary is a friend of mine.', 'pos'),
                     ("I can't believe I'm doing this.", 'neg')]
        self.sentence = "the man a big boos but a bad guy"

    def test_create_url(self):
        result = self.data_pull.create_url(self.graph_url, self.APP_SECRET, self.APP_ID)
        self.assertEqual(result, self.URL1, "url not created")

    def test_render_url_to_json(self):
        result = self.data_pull.render_url_to_json(self.URL)
        self.assertEqual(result, self.url_output, "data not returned")

    def test_scrape_posts_by_date(self):
        result = self.data_pull.scrape_posts_by_date(self.URL1, self.last_crawl, self.POST_DATA, self.APP_ID, self.APP_SECRET)
        self.assertEqual(result, self.scrape_output, "post data not scrape correctly")

    def test_create_comments_url(self):
        result = self.data_pull.create_comments_url(self.graph_url1, self.POST_ID, self.APP_SECRET, self.APP_ID)
        self.assertEqual(result, self.URL2, "url not created")

    def test_get_comments_data(self):
        result = self.data_pull.get_comments_data(self.URL2, self.COMMENT_DATA, self.POST_ID)
        self.assertEqual(result, self.scrape_output, "post data not scrape correctly")

    def test_read_config(self):
        result = self.data_pull.read_config()
        self.assertEqual(result, self.CONFIG_RESULT, "data not read correctly")

    def test_read_data(self):
        result = self.data_pull.read_data(self.config.CONFIG_FILE)
        self.assertEqual(result, self.READ_CONFIG_RESULT, "data not read successfully")

    def test_check_test_data_accuracy(self):
        result = self.classifier.test_data_accuracy()
        self.assertEqual(result, self.TEST_DATA, "mismatch accuracy")

    def test_trainer_sentiment(self):
        result = self.classifier.trainer_sentiment(self.sentence)
        self.assertEqual(result, self.RESULT, "wrong sentence mapping")