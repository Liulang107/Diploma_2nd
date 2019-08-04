import unittest
import Search_criteria
import Search_for_pretenders
import json
from mock import patch
import vk_api

info = []


def setUpModule():
    with open('fixtures/info.json', 'r') as out_info:
        info.extend(json.load(out_info))
    vk_session = vk_api.VkApi(login=info[0]['login'], password=info[0]['password'],
                              api_version='5.101', scope=info[0]['scope'])

    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    global vk
    vk = vk_session.get_api()


class TestVKinder(unittest.TestCase):

    @patch('Search_criteria.input')
    def test_define_search_criteria(self, mock_input):
        mock_input.side_effect = [info[1]['user_input_age_from'],
                                  info[1]['user_input_age_to']]

        result = Search_criteria.define_search_criteria(vk, info[1]['user_input_user'])
        self.assertIsInstance(result, dict)
        self.assertIn('city', result.keys())

    @patch('Search_criteria.input')
    def test_search_for_pretenders(self, mock_input):
        mock_input.side_effect = [info[1]['user_input_age_from'],
                                  info[1]['user_input_age_to']]
        info_dict = Search_criteria.define_search_criteria(vk, info[1]['user_input_user'])

        result = Search_for_pretenders.search_for_pretenders(vk, info_dict)
        self.assertIsInstance(result, list)

    @patch('Search_criteria.input')
    def test_get_top_3_avatars(self, mock_input):
        mock_input.side_effect = [info[1]['user_input_age_from'],
                                  info[1]['user_input_age_to']]
        info_dict = Search_criteria.define_search_criteria(vk, info[1]['user_input_user'])
        pretender_list = Search_for_pretenders.search_for_pretenders(vk, info_dict)

        result = Search_for_pretenders.get_top_3_avatars(vk, pretender_list)
        for items in result:
            self.assertIn('photos', items.keys())
        self.assertEqual(len(result), 10)


if __name__ == '__main__':
    unittest.main()
