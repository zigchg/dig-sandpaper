from digsandpaper import search_server
import unittest
import json
from digsandpaper.engine import Engine
import test_utils


class SearchServerTestCase(unittest.TestCase):

    def setUp(self):
        search_server.app.config['TESTING'] = True
        self.app = search_server.app.test_client()

    def test_hello(self):
        response = self.app.get('/')
        self.assertEquals(200, response.status_code)

    def helper_setup(self, i):
        config = test_utils.load_engine_configuration(i)
        engine = Engine(config)
        query = test_utils.load_sub_configuration("coarse", "preprocess",
                                       i, "_query.json")
        document = test_utils.load_sub_configuration("coarse", "execute",
                                          i, "_document.json")
        es_config = config["coarse"]["execute"]["components"][0]
        test_utils.initialize_elasticsearch([document], es_config)
        search_server.set_engine(engine)
        return (query, es_config)

    def helper_test(self, i):
        (query, es_config) = self.helper_setup(i)
        response = self.app.post('/search', data=json.dumps(query))
        self.assertEquals(200, response.status_code)
        results = json.loads(response.data)
        test_utils.reset_elasticsearch(es_config)
        return results

    def test_search_1(self):
        results_1 = self.helper_test(1)


if __name__ == '__main__':
    unittest.main()
