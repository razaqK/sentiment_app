import unittest
import pulldata
class DataTest(unittest.TestCase):
    def setUp(self):
        self.data_pull = pulldata.PullData()

    def test_data_pull(self):
        self.data_pull.main()


