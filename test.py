import unittest

import datetime

import pulldata
class DataTest(unittest.TestCase):
    def setUp(self):
        self.data_pull = pulldata.PullData()
        self.credentials = self.data_pull.read_config()
        self.graph_url = "https://graph.facebook.com/walmart"
        self.APP_ID = self.credentials[0]
        self.APP_SECRET = self.credentials[1]
        self.last_crawl = datetime.datetime.now() - datetime.timedelta(days=3)
        self.last_crawl = self.last_crawl.isoformat()
        self.URL = "https://graph.facebook.com/walmart/posts/?key=value&" \
                   "access_token=bc5698075f791582c6e5fb9dbc0f144b|2040068469550624"

    def test_create_url(self):
        result = self.data_pull.create_url(self.graph_url, self.APP_ID, self.APP_SECRET)
        self.assertEqual(result, self.URL, "url not created")

    def test_render_url_to_json(self):
        result, status = self.data_pull.render_url_to_json(self.URL)
        self.assertEqual(status, True, "url not created")

    def test_scrape_posts_by_date(self):
        result, status = self.data_pull.scrape_posts_by_date(self.URL, self.last_crawl, self.APP_ID, self.APP_SECRET)
        self.assertEqual(status, True, "url not created")

    def test_main(self):
        status = self.data_pull.main()
        self.assertEqual(status, True, "Data not successfully collected")


