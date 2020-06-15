from unittest import TestCase
from kong_config_builder.utils import remove_none


class TestUtils(TestCase):

    def test_should_remove_none_from_dict(self):
        test_dict = {"key": "value", "other_key": None}
        result = remove_none(test_dict)
        self.assertDictEqual(result, {"key": "value"})

    def test_should_remove_none_from_list(self):
        test_dict = {"key": "value", "other_key": [None, None]}
        result = remove_none(test_dict)
        self.assertDictEqual(result, {"key": "value", "other_key": []})

    def test_should_remove_none_from_dict_inside_dict(self):
        test_dict = {"key": "value", "other_key": {"my_key": None}}
        result = remove_none(test_dict)
        self.assertDictEqual(result, {"key": "value", "other_key": {}})
