import unittest

import datetime

import pulldata
class DataTest(unittest.TestCase):
    def setUp(self):
        self.data_pull = pulldata.PullData()
        self.credentials = self.data_pull.read_config()
        self.graph_url = "https://graph.facebook.com/"
        self.APP_ID = self.credentials[0]
        self.APP_SECRET = self.credentials[1]
        self.last_crawl = datetime.datetime.now() - datetime.timedelta(days=3)
        self.last_crawl = self.last_crawl.isoformat()

    def test_create_url(self):
        self.data_pull.create_url(self.graph_url, self.APP_ID, self.APP_SECRET)

    def test_render_url_to_json(self):
        self.data_pull.render_url_to_json(self.graph_url)

    def test_scrape_posts_by_date(self):
        self.data_pull.scrape_posts_by_date(self.graph_url, self.last_crawl, self.APP_ID, self.APP_SECRET)

    def test_data_pull(self):
        self.data_pull.main()


