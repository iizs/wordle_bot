import configparser
import os
import logging

from requests_oauthlib import OAuth1Session
from .exception import WordleHelperException

logger = logging.getLogger(__name__)


class TwitterHelper:
    DEFAULT_CONFI_DIR = os.path.join(os.getcwd())
    DEFAULT_CONFIG_FILE = 'config.ini'
    REQUEST_METHOD_POST = 'POST'
    REQUEST_METHOD_GET = 'GET'

    API_ROOT = 'https://api.twitter.com'

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read(
            os.path.join(
                TwitterHelper.DEFAULT_CONFI_DIR,
                TwitterHelper.DEFAULT_CONFIG_FILE
            )
        )

        self.oauth1_session = OAuth1Session(
            self.config['twitter']['api_key'],
            client_secret=self.config['twitter']['api_secret_key'],
            resource_owner_key=self.config['twitter']['access_token'],
            resource_owner_secret=self.config['twitter']['access_token_secret'],
        )

    @staticmethod
    def __get_api_url__(api):
        return f'{TwitterHelper.API_ROOT}{api}'

    def __send_api_request__(self, method, api, json_payload=None, params=None):
        url = TwitterHelper.__get_api_url__(api)
        headers = {
            "User-Agent": "WordleBot_Kirin"
        }
        response = self.oauth1_session.request(method, url, params=params, json=json_payload, headers=headers)
        if response.status_code not in (200, 201):
            raise WordleHelperException(response.status_code, response.text)
        return response.json()

    def create_tweet(self, text=None):
        payload = {}
        if text is not None:
            payload['text'] = text
        if len(payload) == 0:
            return

        self.__send_api_request__(
            TwitterHelper.REQUEST_METHOD_POST,
            '/2/tweets',
            json_payload=payload
        )

