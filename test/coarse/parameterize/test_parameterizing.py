import unittest
import json
import codecs
from digsandpaper.coarse.parameterize.parameterizer import Parameterizer
import os


_location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))


def load_json_file(file_name):
    rules = json.load(codecs.open(os.path.join(_location__, file_name),
                                  'r', 'utf-8'))
    return rules


class TestCoarseParameterizing(unittest.TestCase):

    def test_basic_coarse_parameterizing(self):
        config = load_json_file("1_config.json")
        query = load_json_file("1_query.json")
        parameterizer = Parameterizer(config)

        results = parameterizer.parameterize(query)
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]["zone"], [1])
        self.assertEqual(results[1]["zone"], [1, 2])
        self.assertEqual(results[0]["field_count"], 1)
        self.assertEqual(results[1]["field_count"], 1)

    def test_basic_coarse_preprocessing_with_compound_filter(self):
        config = load_json_file("2_config.json")
        query = load_json_file("2_query.json")
        parameterizer = Parameterizer(config)

        result = parameterizer.parameterize(query)
        f = result[0]["SPARQL"]["where"]["filters"][0]
        self.assertEqual(f["clauses"][0]["type"],
                         "owl:Thing")
        self.assertEqual(f["clauses"][1]["type"],
                         "owl:Thing")

    def test_basic_coarse_preprocessing_with_no_type_mapping(self):
        config = load_json_file("3_config.json")
        query = load_json_file("3_query.json")
        parameterizer = Parameterizer(config)

        result = parameterizer.parameterize(query)

    def test_basic_coarse_preprocessing_with_date_filter(self):
        config = load_json_file("4_config.json")
        query = load_json_file("4_query.json")
        parameterizer = Parameterizer(config)

        result = parameterizer.parameterize(query)


if __name__ == '__main__':
    unittest.main()
